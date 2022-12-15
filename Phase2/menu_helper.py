from classes import *


def get_all_buildings(session, show=False):
    """
    If show is True, nicely print out all buildings from the database
    :param session: current session
    :return: a list of all Building objects from the database
    """
    all_buildings = session.query(Building).all()

    if show:
        print("\nAvailable buildings: ")
        for b in all_buildings:
            print("\t" + b.name)

    return all_buildings


def get_all_rooms(session, building_name, show=False):
    """
    If show is True, nicely print out all buildings and rooms from the database
    :param session: current session
    :return: a list of all Room objects from the database
    """
    # Get a list of buildings, rooms from database
    all_rooms = session.query(Room).filter_by(building_name=building_name).all()

    if show:
        # Give the user info about buildings, rooms and employees
        print("\nAvailable rooms: ")
        for r in all_rooms:
            print("\t{0} {1}".format(building_name, r.number))

    return all_rooms


def get_all_employees(session, show=False):
    """
    If show is True nicely print out all employees from the database
    :param session: current session
    :return: a list of all Employee objects from the database
    """
    all_employees = session.query(Employee).all()

    if show:
        print("\nAvailable employees:")
        print("{0: >20}{1: >5}".format("NAME", "ID"))
        for e in all_employees:
            print("{0: >20}{1: >5}".format(e.name, str(e.id)))

    return all_employees


def get_all_hooks(session, show=False):
    """
    If show is True, nicely print out all hooks from the database
    :param session: current session
    :return: a list of all Hook objects from the database
    """
    all_hooks = session.query(Hook).all()

    if show:
        # Print a list of available hooks
        print("\nAvailable hook IDs:")
        for hook in all_hooks:
            print("\t\u26BF " + str(hook.id))

    return all_hooks


def get_all_keys(session, employee_id, show=False):
    # Query to get a list of all keys that this employee has, rule out all returns and losses
    all_keys: [Key] = session.query(Key).join(Loan, Loan.key_id == Key.id) \
        .join(Employee, Employee.id == Loan.employee_id) \
        .filter(Employee.id == employee_id,
                Loan.id.notin_([r.loan_id for r in session.query(Return)]),
                Loan.id.notin_([l.loan_id for l in session.query(Loss)])).all()

    if show:
        print("List of key ids for this employee (that are not returned or lost): ")
        print("\t  {0: >10} {1: >10}".format("KEY ID", "DOOR"))
        for key in all_keys:
            door = session.query(Door).join(Open, Open.door_id == Door.id).join(Hook, Hook.id == Open.hook_id)\
                .join(Key,Key.hook_id == Hook.id).filter(Key.id == key.id).first()
            print("\t\u2705{0: >10} {1: >10} {2} {3}".format(key.id, door.building_name, door.room_number, door.door_name))

    return all_keys


def input_valid_employee_id(session, show=False):
    all_employees = [e.id for e in get_all_employees(session, show)]

    try:
        employee_id = int(input("Enter employee ID: "))
    except ValueError:
        print("Invalid input")
        return None
    if employee_id not in all_employees:
        print("ID not in database")
        return None
    else:
        return employee_id


def input_valid_hook_id(session, show=False):
    # Get a list of hook IDs and show them
    all_hooks: [Hook.id] = [hook.id for hook in get_all_hooks(session, show)]

    # Ask user for hook id, check for invalid input
    try:
        hook_id = int(input("Please enter hook ID: "))
    except ValueError:
        print("Please enter a number!œ")
        return None
    if hook_id not in all_hooks:
        print("Invalid hook ID!")
        return None
    else:
        return hook_id


def input_valid_building(session, show=False):
    all_buildings = [b.name for b in get_all_buildings(session, show)]

    building_name = input("Enter building name: ")
    # Check for valid data
    if building_name not in all_buildings:
        print("Invalid building name!")
        return None

    return building_name


def input_valid_room(session, building_name, show=False):
    get_all_rooms(session, building_name, show)

    try:
        room_number = int(input("Enter room number: "))
    except ValueError:
        print("Invalid input!")
        return None

    # Check for valid data
    if room_number not in [r.number for r in session.query(Room).filter_by(building_name=building_name)]:
        print("Invalid room number!")
        return None

    return room_number


def input_valid_key_id(session, employee_id, show=False):
    all_keys = get_all_keys(session, employee_id, show)

    # Convert to a list of key ids
    all_keys: [Key.id] = [key.id for key in all_keys]

    # Ask for key id and check if valid
    key_id = int(input("Enter key ID: "))
    if key_id not in all_keys:
        # the key are not in the tables
        print("Your information can't be found, try again")
        return None

    return key_id


def input_valid_door(session, building_name, room_number, show=False):
    # List of existing doors
    all_old_doors = session.query(Door.door_name).filter(Door.building_name == building_name,
                                                         Door.room_number == room_number)
    all_old_doors_names = [d.door_name for d in all_old_doors]

    # List of possible door names
    all_new_doors_names = [d.name for d in session.query(DoorName).filter(DoorName.name.notin_(all_old_doors))]

    if show:
        print("\nList of existing doors:")
        for door_name in all_old_doors_names:
            print("\t{0} {1} {2} door".format(building_name, room_number, door_name))

        print("\nList of possible door names:")
        for door_name in all_new_doors_names:
            print("\t" + door_name)

        door_name = input("Enter the new door's name: ")
        if door_name not in all_new_doors_names:
            print("Door not available!")
            return None

        return door_name

    return all_old_doors
