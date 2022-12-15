"""Contains code for each option specified in menu_display.py"""
import time

from bson import ObjectId

from menu_helper import *
from datetime import datetime
from models import *
from relations import *


# 1. Create a key
def create_key():
    all_hooks = hooks_table.find({})
    print("\nCreate a key")
    print("Available hooks")
    for h in all_hooks:
        print("hook: " + str(h["hook"]))
    try:
        hook_id = int(input("Please enter hook id: "))
    except ValueError:
        print("Please enter a number!")
        return None
    else:
        keys(hook_id)
        new_key = key_table.find({})
        key_information = []
        for k in new_key:
            key_information.append(str(k["_id"]))  # storing the ids in array
        print("New key ID created: " + str(key_information.pop()))


# 2. Request access to a given room by a given employee
def request_access():
    """
    Make a request to access a room, takes in the building name, room number and employee id
    If request is approved, call issue_key() to issue the key to said employee
    """
    print("\nREQUEST A KEY")
    building_name = input_valid_building()
    if building_name is None: return
    room_number = input_valid_room(building_name)
    if room_number is None: return
    employee_id = input_valid_employee_id()
    if employee_id is None: return

    # Query to get the hook_id of the front door to the requested room.
    id_front_door_name = door_name.find_one({"door name": "front"})["_id"]
    requested_door = doors_table.find_one(
        {"building name": building_table.find_one({"building name": building_name})["_id"],
         "room": room_table.find_one({"room": room_number})["_id"],
         "door name": id_front_door_name})

    requested_door_hook_id = opens_table.find_one({"door": requested_door["_id"]})["hook"][0]
    requested_door_hook_number = hooks_table.find_one({"_id": requested_door_hook_id})["hook"]

    # Get a set of all hook ids that this employee has, from all keys that he has
    employee_hooks = [key_table.find_one({"_id": key_id})["hook id"] for key_id in get_all_keys(employee_id)]
    employee_hooks = [hooks_table.find_one({"hook": hook_number})["_id"] for hook_number in employee_hooks]

    if requested_door_hook_id in employee_hooks:
        print("\n\u274C ACCESS DENIED\n"
              "You already have access to this room!")
    else:
        # Add a request to the access request table
        access_table.insert_one({"date": datetime.datetime.now(),
                                 "building name": building_name,
                                 "room number": room_number,
                                 "employee id": employee_id})

        # Issue the key
        new_key_id = issue_key(employee_id, requested_door_hook_number)

        # Print success message
        print("\n\u2705 ACCESS GRANTED\n"
              "{0} {1}, front door\n"
              "Key ID: {2}\n"
              "Employee: {3}".format(building_name, room_number, new_key_id,
                                     employee_table.find_one({"_id": employee_id})["employee"]))


# 3. Capture the issue of a key to an employee
def unauthorized_issue_key():
    """
    Called by main() when a user wants to issue a key. They need to make a request first.
    Call request_access()
    """
    print("\nUnauthorized action! Please make a request first\n"
          "Redirecting to make a request...")
    time.sleep(2)
    request_access()


def issue_key(employee_id, hook_id):
    """
    Called by access_request() after a request is granted.

    First, check if a key of a hook is available for loan. If not, create a new key of that hook
    After that, insert a loan into loans table
    """
    # Query a list of available keys (keys that are either not in loan, or in loan and in return)
    all_keys = [key["_id"] for key in key_table.find({"hook id": hook_id})]
    keys_in_loans = [loan["key id"] for loan in loan_table.find({})]
    keys_in_returns = [returns["_id"] for returns in returns_table.find({})]

    available_keys = []
    for key in all_keys:
        if key not in keys_in_loans:
            available_keys.append(key)
        else:
            if key in keys_in_returns:
                available_keys.append(key)

    # Create a new key if none is available
    if available_keys:
        key_id = available_keys[0]
    else:
        key_id = key_table.insert_one({"hook id": hook_id}).inserted_id

    loan_table.insert_one({
        "employee id": employee_id,
        "key id": key_id,
        "start time": datetime.datetime.now()
    })

    return key_id


# 4. Capture losing a key
def losing_key():
    """Get the employee id, get the key id
        look at loans that match that employee id and key id
        get that loan id and give it to lost collection """

    print("\nREPORT A LOST KEY")
    # Ask user for employee and lost key, then validate
    all_employees = loan_table.find({})
    for e in all_employees:
        print("List of employees, key ids and loan ids: " + str(e["employee id"]), str(e["key id"]), str(e["_id"]))

    employee_input = str(input("Please enter the loan id that correlates to your employee id and key id: "))

    loss_information = [

        {"date": datetime.datetime.now()}
    ]
    losses(loss_information)

    losses_id = losses_table.find({})
    loss_info = []
    for i in losses_id:
        loss_info.append(i["_id"])
    pop_losses_id = loss_info.pop()
    loans_to_losses(pop_losses_id, employee_input)
    print("Lost key reported.")


# 5. Report out all the rooms that an employee can enter, given the keys that he/she already has
def accessible_rooms():
    """
    Report out all the rooms that an employee can enter, given the keys that he/she already has
    """
    print("\nREPORT ACCESSIBLE ROOMS")
    # Ask user for a valid employee id, showing them a list of all employees first
    employee_id = input_valid_employee_id()
    if employee_id is None:
        return

    # Get all the hooks that this employee has
    employee_hooks = []
    for key_id in get_all_keys(employee_id):
        hook_number = key_table.find_one({"_id": key_id})["hook id"]
        employee_hooks.append(hooks_table.find_one({"hook": hook_number})["_id"])

    # Get all the opens of this employee
    employee_opens = []
    for hook_id in employee_hooks:
        employee_opens.append(opens_table.find_one({"hook": hook_id}))

    # Get all the doors of this employee
    employee_doors = []
    for open in employee_opens:
        for door_id in open["door"]:
            employee_doors.append(doors_table.find_one({"_id": door_id}))

    print("Accessible rooms:")
    for door in employee_doors:
        print("\t" + building_table.find_one({"_id": door["building name"][0]})["building name"] + " " +
              str(room_table.find_one({"_id": door["room"][0]})["room"]) + " " +
              door_name.find_one({"_id": door["door name"][0]})["door name"])


# 6. Delete a key
def delete_key():
    print("Available Keys")
    # Get cursor object containing all documents in the "employees" collection
    cursor = key_table.find()
    # Iterate over cursor and print each key's ID
    for key in cursor:
        print(f"Key ID: {key['_id']} ")
    # Prompt the user for a key ID to delete
    user_input = str(input("Enter the key id to delete: "))
    # Use a try/except block to handle any errors that may occur
    try:
        # Convert the user's input into a valid Object ID
        key_id = ObjectId(user_input)
        # check if the employee id exists in the collection
        if key_table.find_one({"_id": key_id}):
            # Delete key from key table
            result = key_table.delete_one({"_id": key_id})
            # Delete key reference with loan table
            loan_delete = loan_table.delete_many({"key id": key_id})
            # Check if the references were successfully deleted
            if result.deleted_count > 0 or loan_delete.deleted_count > 0:
                print(
                    f"Successfully deleted {result.deleted_count + loan_delete.deleted_count} references to the key.")
            else:
                print(f"No references to the key '{key_id}' were found in the key_table collection.")

            print(f"Key with id {key_id} has been deleted.")
        else:
            print("Key is not in the database")
    except:
        print("Invalid Input.")


# 7. Delete an employee
def delete_employee():
    print("Available Employees IDs")

    # Get cursor object containing all documents in the "employees" collection
    cursor = employee_table.find()
    # Iterate over cursor and print each employee's ID and name
    for employee in cursor:
        print(f"Name: {employee['employee']}, Employee ID: {employee['_id']} ")
    # Ask user for employee ID to delete
    user_input = input("Enter the employee ID to delete: ")
    # If the employee exists, delete it
    try:
        # Convert the user's input into a valid Object ID
        employee_id = ObjectId(user_input)
        # check if the employee id exists in the collection
        if employee_table.find_one({"_id": employee_id}):
            # delete the employee id in loans table
            loan_delete = loan_table.delete_many({"employee id": employee_id})
            # delete the employee id in access table
            access_delete = access_table.delete_many({"employee id": employee_id})
            # delete the employee id in employee table
            employee_delete = employee_table.delete_many({"_id": employee_id})
            # Check if the references were successfully deleted
            if employee_delete.deleted_count > 0 or loan_delete.deleted_count > 0 \
                    or access_delete.deleted_count > 0:
                print(
                    f"Successfully deleted "
                    f"{employee_delete.deleted_count + loan_delete.deleted_count + access_delete.deleted_count} "
                    f"reference(s) to the employee.")
            else:
                print(f"No references to the employee '{employee_id}' were found in the key_table collection.")
            print(f"Employee with id {employee_id} has been deleted.")
        else:
            print(f"Employee with id {employee_id} is not in the database.")
    except:
        print("Employee id is not valid")


# 8. Add a new door that can be opened by an existing hook
def add_door():
    # Get hook ID and door's info form the user, check for validity
    building_name = input_valid_building()
    if building_name is None: return
    room_number = input_valid_room(building_name)
    if room_number is None: return
    doorname_id = input_valid_doorname(room_number)
    doorname = door_name.find_one({"_id": doorname_id})["door name"]
    if doorname_id is None: return
    hook_number = input_valid_hook_id()
    if hook_number is None: return

    building_id = building_table.find_one({"building name": building_name})["_id"]
    room_id = room_table.find_one({"room": room_number})["_id"]
    hook_id = hooks_table.find_one({"hook": hook_number})["_id"]

    # Add the new door to the database, then get its ID number
    new_door_id = doors_table.insert_one({'building name': [building_id],
                                          'room number': [room_id],
                                          'door name': [doorname_id]}).inserted_id

    # Add the hook ID and door ID to the Open table
    opens_table.insert_one({'hook id': [hook_id], 'door id': [new_door_id]})

    print("\u2705New door created!\n"
          "\t{0} {1} {2} door\n"
          "\tOpened by \u26BF HOOK {3}".format(building_name, room_number, doorname, hook_number))


# 9. Update an access request to move it to a new employee
def update_request():
    all_request = access_table.find({})
    for i in all_request:
        print("Employee ID: ", str(i["employee id"]), "\tAccess ID: ", str(i["_id"]))

    loan_input = str(input("access id you'd like to replace with new user : "))

    all_employees = employee_table.find({})
    for i in all_employees:
        print("All employees: ", str(i["employee"]), str(i["_id"]))
    second_input = str(input("Please enter id of the employee you'd like to add: "))

    from bson.objectid import ObjectId

    _id = ObjectId(loan_input)
    all_updates = {
        "$set": {"employee id": ObjectId(second_input)}
    }
    access_table.update_one({"_id": _id}, all_updates)
    print("New employee has replace old employee in access.")


#  10. Report out all the employees who can get into a room
def report_employees():
    building_name = input_valid_building()
    if building_name is None:
        return
    room_number = input_valid_room(building_name)
    if room_number is None:
        return

    # Get all the doors in this room
    building_id = building_table.find_one({"building name": building_name})["_id"]
    room_id = room_table.find_one({"room": room_number})["_id"]
    all_doors = []
    for door in doors_table.find({"building name": building_id, "room": room_id}):
        all_doors.append(door["_id"])

    # Get all hook_number of those doors
    all_hooks = []
    all_hooks_numbers = []
    all_opens = []
    for door_id in all_doors:
        all_opens.append(opens_table.find_one({"door": door_id}))
    for open in all_opens:
        all_hooks.append(open["hook"])
    for hook_id in all_hooks:
        all_hooks_numbers.append(hooks_table.find_one({"_id": hook_id[0]})["hook"])

    # Go to keys and look for all key_id of those hook_number
    all_keys = []
    for hook_number in all_hooks_numbers:
        for key in key_table.find({"hook id": hook_number}):
            all_keys.append(key["_id"])

    # Go to loan and get all those key_id, that are not in returns or loss
    all_loans = []
    for key_id in all_keys:
        all_loans.append(loan_table.find_one({"key id": key_id}))

    # Go to loan and get the employee id in those filtered loan
    all_employees = []
    for loan in all_loans:
        all_employees.append(loan["employee id"])

    # Go to employee, use the ids to print out the name
    print("Employees that have access:")
    for e_id in all_employees:
        print("\t" + employee_table.find_one({"_id": e_id})["employee"])
