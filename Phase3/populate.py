from relations import *


def populate():
    # populating the building database
    building_information = [
        {"building name": "VEC"},
        {"building name": "ECS"},
        {"building name": "HC"}
    ]
    buildings(building_information)

    # populating the rooms table
    room_information = [{"room": 100}, {"room": 101},
                        {"room": 200}, {"room": 201},
                        {"room": 300}, {"room": 301}
                        ]
    rooms(room_information)

    # creating the relationship between vec building and room
    vec_building = building_table.find({"building name": "VEC"})
    room_search = room_table.find({"room": 100})
    for i in vec_building:
        for j in room_search:
            building_room_relation(i["_id"], j["_id"])

    vec_building_t = building_table.find({"building name": "VEC"})
    room_search_t_t = room_table.find({"room": 101})
    for i in vec_building_t:
        for j in room_search_t_t:
            building_room_relation(i["_id"], j["_id"])

    # creating the relationship between ecs building and room
    ecs_building = building_table.find({"building name": "ECS"})
    ecs_room = room_table.find({"room": 200})
    for i in ecs_building:
        for j in ecs_room:
            building_room_relation(i["_id"], j["_id"])

    ecs_building_t = building_table.find({"building name": "ECS"})
    ecs_room_t = room_table.find({"room": 201})
    for i in ecs_building_t:
        for j in ecs_room_t:
            building_room_relation(i["_id"], j["_id"])

    # creating the relationship between hc building and room
    hc_building = building_table.find({"building name": "HC"})
    hc_room = room_table.find({"room": 300})
    for i in hc_building:
        for j in hc_room:
            building_room_relation(i["_id"], j["_id"])

    hc_building_t = building_table.find({"building name": "HC"})
    hc_room_t = room_table.find({"room": 301})
    for i in hc_building_t:
        for j in hc_room_t:
            building_room_relation(i["_id"], j["_id"])

    name_information = [{"door name": "front"},
                        {"door name": "back"},
                        {"door name": "south"},
                        {"door name": "east"}
                        ]
    door_name_table(name_information)

    # creating the door collection and the relationship
    door_information = [
        {"door": 1},
        {"door": 2},
        {"door": 3},
        {"door": 4},
        {"door": 5},
        {"door": 6}

    ]
    doors(door_information)

    doors_id = doors_table.find({"door": 1})
    door_room = room_table.find({"room": 100})
    door_building = building_table.find({"building name": "VEC"})
    door_n = door_name.find({"door name": "front"})

    for i in doors_id:
        for j in door_building:
            for k in door_room:
                for p in door_n:
                    door_relations(i["_id"], j["_id"], p["_id"], k["_id"])

    doors_id_t = doors_table.find({"door": 2})
    door_room_t = room_table.find({"room": 101})
    door_building_t = building_table.find({"building name": "VEC"})
    door_n_t = door_name.find({"door name": "front"})

    for i in doors_id_t:
        for j in door_building_t:
            for k in door_room_t:
                for p in door_n_t:
                    door_relations(i["_id"], j["_id"], p["_id"], k["_id"])

    doors_id_th = doors_table.find({"door": 3})
    door_room_th = room_table.find({"room": 200})
    door_building_th = building_table.find({"building name": "ECS"})
    door_n_th = door_name.find({"door name": "front"})

    for i in doors_id_th:
        for j in door_building_th:
            for k in door_room_th:
                for p in door_n_th:
                    door_relations(i["_id"], j["_id"], p["_id"], k["_id"])

    doors_id_f = doors_table.find({"door": 4})
    door_room_f = room_table.find({"room": 201})
    door_building_f = building_table.find({"building name": "ECS"})
    door_n_f = door_name.find({"door name": "front"})

    for i in doors_id_f:
        for j in door_building_f:
            for k in door_room_f:
                for p in door_n_f:
                    door_relations(i["_id"], j["_id"], p["_id"], k["_id"])

    doors_id_fi = doors_table.find({"door": 5})
    door_room_fi = room_table.find({"room": 300})
    door_building_fi = building_table.find({"building name": "HC"})
    door_n_fi = door_name.find({"door name": "front"})

    for i in doors_id_fi:
        for j in door_building_fi:
            for k in door_room_fi:
                for p in door_n_fi:
                    door_relations(i["_id"], j["_id"], p["_id"], k["_id"])

    doors_id_s = doors_table.find({"door": 6})
    door_room_s = room_table.find({"room": 301})
    door_building_s = building_table.find({"building name": "HC"})
    door_n_s = door_name.find({"door name": "front"})

    for i in doors_id_s:
        for j in door_building_s:
            for k in door_room_s:
                for p in door_n_s:
                    door_relations(i["_id"], j["_id"], p["_id"], k["_id"])

    hook_insertion = [{"hook": 1},
                      {"hook": 2},
                      {"hook": 3},
                      {"hook": 4}
                      ]
    hooks(hook_insertion)

    opens_insertion = [{"opens": 1},
                       {"opens": 2},
                       {"opens": 3},
                       {"opens": 4}
                       ]
    opens(opens_insertion)

    doors_opens = doors_table.find({"door": 1})
    hooks_open = hooks_table.find({"hook": 1})
    opens_opens = opens_table.find({"opens": 1})

    for i in doors_opens:
        for j in hooks_open:
            for k in opens_opens:
                door_to_hook_open(k["_id"], j["_id"], i["_id"])

    doors_opens_t = doors_table.find({"door": 2})
    hooks_open_t = hooks_table.find({"hook": 1})
    opens_opens_t = opens_table.find({"opens": 1})

    for i in doors_opens_t:
        for j in hooks_open_t:
            for k in opens_opens_t:
                door_to_hook_open(k["_id"], j["_id"], i["_id"])

    doors_opens_th = doors_table.find({"door": 3})
    hooks_open_th = hooks_table.find({"hook": 2})
    opens_opens_th = opens_table.find({"opens": 2})

    for i in doors_opens_th:
        for j in hooks_open_th:
            for k in opens_opens_th:
                door_to_hook_open(k["_id"], j["_id"], i["_id"])

    doors_opens_f = doors_table.find({"door": 4})
    hooks_open_f = hooks_table.find({"hook": 2})
    opens_opens_f = opens_table.find({"opens": 2})

    for i in doors_opens_f:
        for j in hooks_open_f:
            for k in opens_opens_f:
                door_to_hook_open(k["_id"], j["_id"], i["_id"])

    doors_opens_fi = doors_table.find({"door": 5})
    hooks_open_fi = hooks_table.find({"hook": 3})
    opens_opens_fi = opens_table.find({"opens": 3})

    for i in doors_opens_fi:
        for j in hooks_open_fi:
            for k in opens_opens_fi:
                door_to_hook_open(k["_id"], j["_id"], i["_id"])

    doors_opens_s = doors_table.find({"door": 6})
    hooks_open_s = hooks_table.find({"hook": 4})
    opens_opens_s = opens_table.find({"opens": 4})

    for i in doors_opens_s:
        for j in hooks_open_s:
            for k in opens_opens_s:
                door_to_hook_open(k["_id"], j["_id"], i["_id"])

    employee_insertion = [{"employee": "David Brown"},
                          {"employee": "Steven Gold"},
                          {"employee": "Kite Nyguyen"}
                          ]
    employees(employee_insertion)
