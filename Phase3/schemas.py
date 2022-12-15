from models import *

building_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["building name"],
        "properties": {
            "building name": {
                "bsonType": "string",
                "description": "building name"
            },
            "room": {
                "bsonType": "double",
                "description": "room number"
            }
        }
    }
}

building_table.command("collMod", "building", validator=building_validator)

room_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["building name", "room"],
        "properties": {
            "building name": {
                "bsonType": "string",
                "description": "building name"
            },
            "room number": {
                "bsonType": "double",
                "description": "room number"
            }
        }
    }
}
room_table.command("collMod", "rooms", validator=room_validator)

doors_name_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["door name"],
        "properties": {
            "door name": {
                "bsonType": "string",
                "description": "door name"
            }
        }
    }
}

door_name.command("collMod", "door name", validator=doors_name_validator)

doors_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["door name", "room", "building name"],
        "properties": {
            "building name": {
                "bsonType": "string",
                "description": "building name"
            },
            "room": {
                "bsonType": "double",
                "description": "room number"
            },
            "door name": {
                "bsonType": "string",
                "description": "door name"
            }
        }
    }
}

doors_table.command("collMod", "access request", validator=doors_validator)

access_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["date", "room number", "building name", "employee id"],
        "properties": {
            "building name": {
                "bsonType": "string",
                "description": "building name"
            },
            "room number": {
                "bsonType": "double",
                "description": "room number"
            },
            "date": {
                "bsonType": "date",
                "description": "the day the request happened"
            },
            "employee_id": {
                "bsonType": "objectId",
                "description": "the id of the employee"
            }
        }
    }
}

access_table.command("collMod", "access request", validator=access_validator)

employee_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["employee id"],
        "properties": {
            "employee_id": {
                "bsonType": "objectId",
                "description": "the id of the employee"
            }
        }
    }
}

employee_table.command("collMod", "employee", validator=employee_validator)

loan_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["employee id", "key id", "start time"],
        "properties": {
            "employee id": {
                "bsonType": "objectId",
                "description": "the id of the employee"
            },
            "key id": {
                "bsonType": "objectId",
                "description": "the key id issued"
            },
            "start time": {
                "bsonType": "timestamp",
                "description": "the timestamp of when the key was issued"
            }
        }
    }
}

loan_table.command("collMod", "loan", validator=employee_validator)

return_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["loan id", "date"],
        "properties": {
            "loan id": {
                "bsonType": "objectId",
                "description": "the id of the loan"
            },
            "date": {
                "bsonType": "date",
                "description": "the date of the return"
            }
        }
    }
}

returns_table.command("collMod", "returns", validator=return_validator)

loss_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["loan id", "date"],
        "properties": {
            "loan id": {
                "bsonType": "objectId",
                "description": "the id of the loan"
            },
            "date": {
                "bsonType": "date",
                "description": "the date of the loss"
            }
        }
    }
}

losses_table.command("collMod", "loss", validator=loss_validator)

key_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["hook id"],
        "properties": {
            "hook id": {
                "bsonType": "objectId",
                "description": "the id of the hook"
            }
        }
    }
}

key_table.command("collMod", "key", validator=key_validator)

open_validator = {
    "jsonSchema": {
        "bsonType": "object",
        "required": ["hook id", "door_id"],
        "properties": {
            "hook id": {
                "bsonType": "objectId",
                "description": "the id of the hook"
            },
            "door id": {
                "bsonType": "objectId",
                "description": "the id of the door"

            }
        }
    }
}

opens_table.command("collMod", "open", validator=open_validator)
