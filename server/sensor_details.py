

room_details_001 = { "id":"room_001", "temperature": 1.0, "humidity": 135.0, "co2": 100 }
room_details_002 = { "id":"room_002", "temperature": 2.0, "humidity": 22.0, "co2": 200 }
room_details_003 = { "id":"room_003", "temperature": 3.0, "humidity": 522.0, "co2": 400 }
rooms = [room_details_001, room_details_002, room_details_003]


def get_all_sensors():
    return rooms


if __name__ == '__main__':
    # print(type(rooms))
    # print(rooms)

    # print(type(room_details_001))
    # print(room_details_001)

    print(get_all_sensors())
