from models import *


# DONE
def get_all_buildings(show=False):
    """
    If show is True, nicely print out all buildings from the database
    :return: a list of all Building objects from the database
    """
    all_buildings = building_table.find({})

    if show:
        print("\nAvailable buildings: ")
        for b in all_buildings:
            print("\t" + b["building name"])

    return building_table.find({})


# DONE
def get_all_rooms(show=False):
    """
    If show is True, nicely print out all buildings and rooms from the database
    :return: a list of all Room objects from the database
    """
    # Get a list of buildings, rooms from database
    all_buildings = get_all_buildings(show=False)
    all_rooms = room_table.find({})

    if show:
        # Give the user info about buildings, rooms and employees
        print("\nAvailable rooms: ")
        for b in all_buildings:
            print("\t" + b["building name"])

            for room_id in b["room"]:
                r = room_table.find_one({"_id": room_id})
                print("\t\t" + str(r["room"]))

    return all_rooms


# DONE
def get_all_employees(show=False):
    """
    If show is True nicely print out all employees from the database
    :return: a list of all Employee objects from the database
    """
    all_employees = employee_table.find({})

    if show:
        print("\nAvailable employees:")
        for e in all_employees:
            for i in all_employees:
                print("\t" + e["employee"])
                print("\t" + i["_id"])

    return all_employees


def get_all_hooks(show=False):
    """
    If show is True, nicely print out all hooks from the database
    :return: a list of all Hook objects from the database
    """
    all_hooks = hooks_table.find({})

    if show:
        # Print a list of available hooks
        print("\nAvailable hook IDs:")
        for hook in all_hooks:
            print("\t\u26BF " + str(hook["_id"]))

    return all_hooks


# DONE
def get_all_keys(employee_id, show=False):
    # Query to get a list of all keys that this employee has, rule out all returns and losses
    all_loans = [loan for loan in loan_table.find({"employee id": employee_id})]
    all_returns = [r["loan id"] for r in returns_table.find({})]
    all_losses = [l["loan id"] for l in losses_table.find({})]

    available_keys = []
    for loan in all_loans:
        if loan["_id"] not in all_returns and loan["_id"] not in all_losses:
            available_keys.append(loan["key id"])

    if show:
        print("List of key ids for this employee (that are not returned or lost): ")
        for key in available_keys:
            print(key)
        # print("\t  {0: >10} {1: >10}".format("KEY ID", "DOOR"))
        # for key in all_keys:
        #     door = session.query(Door).join(Open, Open.door_id == Door.id).join(Hook, Hook.id == Open.hook_id) \
        #         .join(Key, Key.hook_id == Hook.id).filter(Key.id == key.id).first()
        #     print("\t\u2705{0: >10} {1: >10} {2} {3}".format(key.id, door.building_name, door.room_number,
        #                                                      door.door_name))

    return available_keys


# DONE
def input_valid_employee_id():
    all_employees_names = [e["employee"] for e in employee_table.find({})]
    print("Available employees:")
    for name in all_employees_names:
        print("\t" + name)

    employee_name = input("Enter employee name: ")
    if employee_name not in all_employees_names:
        print("Employee not in database")
        return None
    else:
        return employee_table.find_one({"employee": employee_name})["_id"]


# DONE
def input_valid_hook_id():
    # Get a list of hook IDs and show them
    all_hooks = hooks_table.find({})
    for h in all_hooks:
        print(f"Available hook id:" + str(h["hook"]))

    # Ask user for hook id, check for invalid input
    try:
        hook_id = int(input("Please enter hook ID: "))
    except ValueError:
        print("Please enter a number!")
        return None
    else:
        return hook_id


# DONE
def input_valid_building():
    all_buildings = [b["building name"] for b in get_all_buildings(show=True)]

    building_name = input("Enter building name: ")
    # Check for valid data
    if building_name not in all_buildings:
        print("Invalid building name!")
        return None

    return building_name


# DONE
def input_valid_room(building_name):
    print("\t" + building_name +
          "\nAvailable rooms")
    all_rooms = []
    for room_id in building_table.find_one({"building name": building_name})["room"]:
        r = room_table.find_one({"_id": room_id})
        print("\t\t" + str(r["room"]))
        all_rooms.append(r["room"])

    try:
        room_number = int(input("Enter room number: "))
    except ValueError:
        print("Invalid input!")
        return None

    # Check for valid data
    if room_number not in all_rooms:
        print("Invalid room number!")
        return None

    return room_number


def input_valid_doorname(room_number):
    """
    Return a valid doorname id  in a particular room, rule out the doors that already exist
    :param room_number: the room number
    :return: a valid doorname id
    """
    room_id = room_table.find_one({"room": room_number})["_id"]

    all_old_doors = []
    for old_door in doors_table.find({"room": room_id}):
        all_old_doors.append(old_door["door name"][0])

    valid_doornames = []
    for doorname in door_name.find({}):
        if doorname["_id"] not in all_old_doors:
            valid_doornames.append(doorname["door name"])

    print("\nList of possible doors for this room:")
    for doorname in valid_doornames:
        print("\t" + doorname)

    user_input = input("Please enter a door name: ")
    if user_input not in valid_doornames:
        print("Door not available!")
        return None

    return door_name.find_one({"door name": user_input})["_id"]



