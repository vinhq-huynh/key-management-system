"""
A function to populate some tables in the database.
This assumes that all relationships and constraints are already implemented outside of Python.
"""
from classes import *


def populate(session):

    # Check if data is already in the database
    if session.query(Building).count() != 0:
        print("\nDATA ALREADY IN DATABASE!")
        return

    # Populate buildings
    buildings = [Building("VEC"), Building("ECS"), Building("HC")]
    for b in buildings:
        session.add(b)
    session.commit()

    # Populate rooms
    rooms = [Room("VEC", 100), Room("VEC", 101),
             Room("ECS", 308), Room("ECS", 524),
             Room("HC", 120), Room("HC", 121)]
    for r in rooms:
        session.add(r)
    session.commit()

    # Populate door_names
    door_names = [DoorName("front"), DoorName("back"), DoorName("south")]
    for d in door_names:
        session.add(d)
    session.commit()

    # Populate doors
    doors = [Door("VEC", 100, "front"),
             Door("VEC", 101, "front"),
             Door("ECS", 308, "front"),
             Door("ECS", 524, "front"),
             Door("HC", 120, "front"),
             Door("HC", 121, "front"),
             Door("HC", 121, "back")]
    for d in doors:
        session.add(d)
    session.commit()

    # Populate employees
    employees = [Employee("David Brown"),
                 Employee("Neal Terrell"),
                 Employee("Steven Gold"),
                 Employee("Darin Goldstein"),
                 Employee("Dave Winter"),
                 Employee("Dwayne Johnson")]
    for e in employees:
        session.add(e)
    session.commit()

    # Populate hooks
    hooks = [Hook(), Hook(), Hook(), Hook()]
    for h in hooks:
        session.add(h)
    session.commit()

    # Populate opens
    opens = [Open(hook_id=1, door_id=1), Open(hook_id=1, door_id=2),
             Open(hook_id=2, door_id=3), Open(hook_id=2, door_id=4),
             Open(hook_id=3, door_id=5),
             Open(hook_id=4, door_id=6), Open(hook_id=4, door_id=7)]
    for o in opens:
        session.add(o)
    session.commit()

    print("\nDATABASE IS POPULATED!")

