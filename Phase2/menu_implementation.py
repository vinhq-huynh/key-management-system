"""Contains code for each option specified in menu_display.py"""
import time
from menu_helper import *
from sqlalchemy import Integer, or_
from sqlalchemy import update

from datetime import datetime


# 1. Create a key
def create_key(session, hook_id=None) -> Integer:
    """
    Add a key to the 'keys' table, requires the hook_id of the hook that this new key belongs to
    :param: hook_id is either passed directly from a call, or is input from the console by user
    :return: The newly created key's id
    """
    print("\nCREATE A KEY")
    # If hook_id is not available, get it from the user
    if hook_id is None:
        hook_id = input_valid_hook_id(session, show=True)
        if hook_id is None: return

    # Add a new key, return key id of new key
    new_key = Key(hook_id)
    session.add(new_key)
    session.commit()
    print("\nSuccess. A key of hook {0} created!\n"
          "New key ID: {1}".format(hook_id, new_key.id))

    return new_key.id


# 2. Request access to a given room by a given employee
def request_access(session):
    """
    Make a request to access a room, takes in the building name, room number and employee id
    If request is approved, call issue_key() to issue the key to said employee
    """
    # Show user all info about buildings, rooms, and employees
    # And ask user to give info about a request
    print("\nREQUEST A KEY")
    building_name = input_valid_building(session, show=True)
    if building_name is None: return
    room_number = input_valid_room(session, building_name, show=True)
    if room_number is None: return
    employee_id = input_valid_employee_id(session, show=True)
    if employee_id is None: return

    # Check the request to grant access
    # Query to get the hook_id of the front door to the requested room. Using inner joins.
    front_door_hook_id = session.query(Open).join(Door, Door.id == Open.door_id) \
        .join(Room, Room.number == Door.room_number) \
        .join(Building) \
        .filter(Building.name == building_name,
                Room.number == room_number,
                Door.door_name == "front").first().hook_id

    # Query to get a list of all keys that this employee has, rule out all returns and losses
    all_keys: [Key] = get_all_keys(session, employee_id)

    # Get a set of all hook ids that this employee has, from all keys that he has
    employee_hooks: {Hook.id} = {key.hook_id for key in all_keys}

    # Grant access if the employee doesn't have the door's hook id yet
    if front_door_hook_id in employee_hooks:
        print("\n\u274C ACCESS DENIED\n"
              "You already have access to this room!")
    else:
        # Add a request to the access request table
        session.add(AccessRequest(datetime.now(), room_number, building_name, employee_id))

        # Issue the key
        new_key_id = issue_key(session, employee_id, front_door_hook_id)

        # Print success message
        employee_name = session.query(Employee).filter_by(id=employee_id).first().name
        print("\n\u2705 ACCESS GRANTED\n"
              "{0} {1}, front door\n"
              "Key ID: {2}\n"
              "Employee: {3}".format(building_name, room_number, new_key_id, employee_name))


# 3. Capture the issue of a key to an employee
def unauthorized_issue_key(session):
    """
    Called by main() when a user wants to issue a key. They need to make a request first.
    Call request_access()
    """
    print("\nUnauthorized action! Please make a request first\n"
          "Redirecting to make a request...")
    time.sleep(2)
    request_access(session)


def issue_key(session, employee_id, hook_id) -> Integer:
    """
    Called by access_request() after a request is granted.

    First, check if a key of a hook is available for loan. If not, create a new key of that hook
    After that, insert a loan into loans table
    """
    # Query a list of available keys (keys that are either not in loan, or in loan and in return)
    available_keys: [Key] = session.query(Key).outerjoin(Loan, Loan.key_id == Key.id) \
        .filter(Key.hook_id == hook_id,
                or_(Loan.id == None,
                    Loan.id.in_([r.loan_id for r in session.query(Return)]))).all()
    # Convert the list of Keys object to a list of key ids
    available_keys: [Key.id] = [key.id for key in available_keys]

    # Create a new key if none is available
    if available_keys:
        key_id = available_keys[0]
    else:
        key_id = create_key(session, hook_id)

    new_loan = Loan(employee_id=employee_id, key_id=key_id, start_time=datetime.now())
    session.add(new_loan)
    session.commit()

    return key_id


# 4. Capture losing a key
def losing_key(session):
    print("\nREPORT A LOST KEY")
    # Ask user for employee and lost key, then validate
    employee_id = input_valid_employee_id(session, show=True)
    if employee_id is None: return

    lost_key_id = input_valid_key_id(session, employee_id, show=True)
    if lost_key_id is None: return

    # Get hook id for the lost key
    hook_id = session.query(Key).filter_by(id=lost_key_id).first().hook_id

    # Add a loss
    print("Adding lost key to loss")

    loan_id = session.query(Loan).filter_by(key_id=lost_key_id).first().id

    lost_key = Loss(loan_id, datetime.now())  # <- adding the lost key to the loss table
    session.add(lost_key)
    session.commit()

    # Issuing a new key
    print("Issuing new key")
    new_key_id = issue_key(session, employee_id, hook_id)
    print("New key ID {0} issued\n".format(new_key_id))

    # Print the list again to check
    get_all_keys(session, employee_id, show=True)


# 5. Report out all the rooms that an employee can enter, given the keys that he/she already has
def accessible_rooms(session):
    """
    Report out all the rooms that an employee can enter, given the keys that he/she already has
    """
    # Print out all employees from database
    print("\nREPORT ACCESSIBLE ROOMS")
    # Ask user for a valid employee id, showing them a list of all employees first
    employee_id = input_valid_employee_id(session, show=True)
    if employee_id is None:
        return

    print("\nEmployee: " + session.query(Employee).filter_by(id=employee_id).first().name)
    print("Accessible rooms:")
    get_all_keys(session, employee_id, show=True)


# 6. Delete a key
def delete_key(session):
    # Query access to all the tables
    loans_table = session.query(Loan)
    keys_table = session.query(Key)
    return_table = session.query(Return)
    losses_table = session.query(Loss)

    # Generate lists of the tables we want to irritate through
    all_loan_id_in_returns_table = [returns.loan_id for returns in return_table]
    all_loan_id_in_losses_table = [losses.loan_id for losses in losses_table]
    all_key_id_in_loans_table = [loans.key_id for loans in loans_table]
    all_key_id_in_keys_table = [keys.id for keys in keys_table]

    # List out the available keys id
    print("Available keys ID:")
    for k in keys_table:
        print("{0: >20}".format(str(k.id)))
    # ask user which key_id they want to delete
    try:
        key_input = int(input("Enter key ID: "))
    except ValueError:
        print("Invalid input")
        return
    if key_input not in all_key_id_in_keys_table:
        print("ID not in database")
        return
    else:
        if key_input in all_key_id_in_loans_table:
            all_loans = session.query(Loan).filter_by(key_id=key_input).all()
            for loan in all_loans:

                if loan.id in all_loan_id_in_losses_table:
                    session.query(Loss).filter_by(loan_id=loan.id).delete()
                    session.commit()

                # Check if loan id is in return table
                elif loan.id in all_loan_id_in_returns_table:
                    session.query(Return).filter_by(loan_id=loan.id).delete()
                    session.commit()

            print("loan id is deleted in losses/returns table")

            loans_table.filter_by(key_id=key_input).delete()
            session.commit()
            print("loan id is deleted using given key id")

        keys_table.filter_by(id=key_input).delete()
        session.commit()
        print("Key has been deleted")


# 7. Delete an employee
def delete_employee(session):

    employee_id = input_valid_employee_id(session, show=True)

    # Get employee_id from user and validate
    all_employee_id_in_loan_table = [loan.employee_id for loan in session.query(Loan)]
    all_loan_id_in_returns_table = [returns.loan_id for returns in session.query(Return)]
    all_loan_id_in_losses_table = [losses.loan_id for losses in session.query(Loss)]
    all_employee_id_in_access_table = [access.employee_id for access in session.query(AccessRequest)]

    # Check if employee borrow a key first,
    # so it won't violate constraint when deleted
    if employee_id in all_employee_id_in_loan_table:
        # want to get loan id using reference from user input
        all_loans = session.query(Loan).filter_by(employee_id=employee_id).all()
        for loan in all_loans:
            # Check if loan id is in losses table
            if loan.id in all_loan_id_in_losses_table:
                session.query(Loss).filter_by(loan_id=loan.id).delete()
                session.commit()

            # Check if loan id is in return table
            elif loan.id in all_loan_id_in_returns_table:
                session.query(Return).filter_by(loan_id=loan.id).delete()
                session.commit()

        session.query(Loan).filter_by(employee_id=employee_id).delete()
        session.commit()

    print("Employee's loan is deleted in return and loss table")
    print("Employee's loan is deleted in loans table")

    # Check if employee id is in access table
    if employee_id in all_employee_id_in_access_table:
        session.query(AccessRequest).filter_by(employee_id=employee_id).delete()
        session.commit()
        print("Employee's request is deleted in request table")

    session.query(Employee).filter_by(id=employee_id).delete()
    session.commit()
    print("Employee has been deleted")


# 8. Add a new door that can be opened by an existing hook
def add_door(session):
    # Get hook ID and door's info form the user, check for validity
    building_name = input_valid_building(session, show=True)
    if building_name is None: return
    room_number = input_valid_room(session, building_name, show=True)
    if room_number is None: return
    door_name = input_valid_door(session, building_name, room_number, show=True)
    if door_name is None: return
    hook_id = input_valid_hook_id(session, show=True)
    if hook_id is None: return

    # Add the new door to the database and add the hook ID and door ID to the Open table
    new_door = Door(building_name, room_number, door_name)
    session.add(new_door)
    session.add(Open(hook_id, new_door.id))
    session.commit()

    print("\u2705New door created!\n"
          "\t{0} {1} {2} door\n"
          "\tOpened by \u26BF HOOK {3}".format(building_name, room_number, door_name, hook_id))


# 9. Update an access request to move it to a new employee
def update_request(session):
    employee_access = session.query(Employee).join(AccessRequest, Employee.id == AccessRequest.employee_id)

    for e1 in employee_access:
        print(f"{e1.id}:{e1.name}")  # lists the emp names and their ids
    print("Enter the employee ID that you want to remove from Access Request")
    old_employee = input_valid_employee_id(session, False)  # list of old employees to be removed
    all_employees = session.query(Employee).filter(Employee.id != old_employee)  # get the
    # ids in emp that r not the old emp id
    for e2 in all_employees:
        print(f"{e2.id}:{e2.name}")  # list of all the emp
    print("Enter the employee ID that you want to have Access Request")
    new_employee = input_valid_employee_id(session, False)  # list of valid ids

    # update the access request for new employee
    update_r = update(AccessRequest).where(AccessRequest.employee_id == old_employee).values(
        date=datetime.now(), employee_id=new_employee)
    # enables us to swap
    session.execute(update_r)

    session.commit()
    print("New Employee now has Access Request")


#  10. Report out all the employees who can get into a room
def report_employees(session):
    building_name = input_valid_building(session, show=True)
    if building_name is None:
        return
    room_number = input_valid_room(session, building_name, show=True)
    if room_number is None:
        return

    all_employees = session.query(Employee).join(Loan, Loan.employee_id == Employee.id) \
        .join(Key, Key.id == Loan.key_id).join(Hook, Hook.id == Key.hook_id) \
        .join(Open, Open.hook_id == Hook.id).join(Door, Door.id == Open.door_id).filter(
        Door.building_name == building_name,
        Door.room_number == room_number)

    print("All employees that has access to this room:")
    for e in all_employees:
        print("\t{0}: {1}".format(e.id, e.name))
