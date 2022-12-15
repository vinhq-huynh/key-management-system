from models import *


def building_room_relation(building_id, room_id):
    from bson.objectid import ObjectId
    _id = ObjectId(building_id)
    building_table.update_one({"_id": _id}, {"$addToSet": {'room': room_id}})


def door_relations(door_id, building_id, name_id, room_id):
    from bson.objectid import ObjectId
    _id = ObjectId(door_id)
    doors_table.update_one({"_id": _id}, {"$addToSet": {"building name": building_id}})
    doors_table.update_one({"_id": _id}, {"$addToSet": {"door name": name_id}})
    doors_table.update_one({"_id": _id}, {"$addToSet": {"room": room_id}})


def room_to_access(access_id, building_id, room_id):
    from bson.objectid import ObjectId
    _id = ObjectId(access_id)
    doors_table.update_one({"_id": _id}, {"$addToSet": {"building name": building_id}})
    doors_table.update_one({"_id": _id}, {"$addToSet": {"room": room_id}})


def employee_to_access(access_id, employee_id):
    from bson.objectid import ObjectId
    _id = ObjectId(access_id)
    doors_table.update_one({"_id": _id}, {"$addToSet": {"employee": employee_id}})


def employee_to_loans(employee_id, key_id):
    from bson.objectid import ObjectId
    _id = ObjectId()
    doors_table.update_one({"_id": _id}, {"$addToSet": {"employee": employee_id}})
    doors_table.update_one({"_id": _id}, {"$addToSet": {"key id": key_id}})
    doors_table.update_one({"_id": _id}, {"$addToSet": {"time": datetime.datetime.now()}})


def hook_to_key(primary_hook, secondary_hook):
    from bson.objectid import ObjectId
    _id = ObjectId(primary_hook)
    doors_table.update_one({"_id": _id}, {"$addToSet": {"key id": secondary_hook}})


def door_to_hook_open(open_id, hook_id, door_id):
    from bson.objectid import ObjectId
    _id = ObjectId(open_id)
    opens_table.update_one({"_id": _id}, {"$addToSet": {"hook": hook_id}})
    opens_table.update_one({"_id": _id}, {"$addToSet": {"door": door_id}})


def loans_to_returns(returns_id, loans_id):
    from bson.objectid import ObjectId
    _id = ObjectId(returns_id)
    returns_table.update_one(({"_id": _id}, {"$addToSet": {"loan id": loans_id}}))


def loans_to_losses(loss_id, loans_id):
    from bson.objectid import ObjectId
    _id = ObjectId(loss_id)
    losses_table.update_one({"_id": _id}, {"$addToSet": {"loan id": ObjectId(loans_id)}})

