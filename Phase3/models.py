from pymongo import MongoClient
import datetime

cluster = 'mongodb+srv://stephen7777:twerkteamA12@cluster0.3ja9x3k.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(cluster)
project_database = client["phase_three"]
building_table = project_database['building']
room_table = project_database["rooms"]
door_name = project_database["door name"]
doors_table = project_database["doors"]
hooks_table = project_database["hooks"]
opens_table = project_database["opens"]
employee_table = project_database["employee"]
loan_table = project_database["loans"]
access_table = project_database["request"]
key_table = project_database["keys"]
losses_table = project_database['losses']
returns_table = project_database["returns"]


def buildings(building_information):
    building_table.insert_many(building_information)


def rooms(room_information):
    room_table.insert_many(room_information)


def door_name_table(name_information):
    door_name.insert_many(name_information)


def doors(door_information):
    doors_table.insert_many(door_information)


def hooks(hook_information):
    hooks_table.insert_many(hook_information)


def opens(opens_information):
    opens_table.insert_many(opens_information)


def employees(employees_information):
    employee_table.insert_many(employees_information)


def access_request(access_request_information):
    access_table.insert_many(access_request_information)


def loan(loan_information):
    loan_table.update_many(loan_information)


def returns(returns_information):
    returns_table.insert_many(returns_information)


def losses(losses_information):
    losses_table.insert_many(losses_information)


def keys(new_key):
    key_information = {"hook id": new_key}
    key_table.insert_one(key_information)