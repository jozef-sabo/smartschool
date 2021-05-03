import mysql.connector
import datetime
import re

# SECRETS IMPORT
# DATABASE_HOST = ""
# DATABASE_PORT = 0
# DATABASE_NAME = ""
# DATABASE_USER = ""
# DATABASE_PASSWORD = ""
L_DATABASE_NAME = ""
L_DATABASE_USER = ""
L_DATABASE_PASSWORD = ""
try:
    from secrets import *
except ImportError:
    pass



"""  STARY SPOSOB
room_details_001 = {"id": "room_001", "temperature": 1.0, "humidity": 135.0, "co2": 100}
room_details_002 = {"id": "room_002", "temperature": 2.0, "humidity": 22.0, "co2": 200}
room_details_003 = {"id": "room_003", "temperature": 3.0, "humidity": 522.0, "co2": 400}
rooms = [room_details_001, room_details_002, room_details_003]
"""

units = {}


def get_all_sensors():
    connection = mysql.connector.connect(host=DATABASE_HOST, database=DATABASE_NAME, user=DATABASE_USER,
                                         password=DATABASE_PASSWORD, port=DATABASE_PORT)
    # connection = mysql.connector.connect(host="localhost", database=L_DATABASE_NAME, user=L_DATABASE_USER,
    #                                      password=L_DATABASE_PASSWORD)
    cursor = connection.cursor()

    """ AK BY SENZORY POSIELALI V CASE (limitne) BLIZIACOM SA datetime A POSIEALI BY VSETKY
    cursor.execute("SELECT `room_number`, `sensor_type`, `sensor_value`, `sensor_unit` FROM `rooms` r WHERE r.`date_time` ="
                   " (SELECT r.`date_time` FROM `rooms` r ORDER BY r.`date_time` DESC LIMIT 1) ORDER BY `room_number`")
    """

    cursor.execute("SELECT DISTINCT `room_number` FROM `rooms`  WHERE 1")
    classes = cursor.fetchall()

    data = {}
    for the_class in classes:
        class_id = the_class[0]
        data[class_id] = {}
        cursor.execute(
            "SELECT `sensor_type`, `sensor_value`, `sensor_unit`, `date_time` FROM `rooms` r WHERE `room_number` = '%s'"
            "AND r.`date_time` = (SELECT r.`date_time` FROM `rooms` r WHERE `room_number` = '%s' ORDER BY "
            "r.`date_time` DESC LIMIT 1)" % (class_id, class_id))

        for row in cursor:
            sensor_type, sensor_value, sensor_unit, date_time, *garbage = row
            data[class_id][sensor_type] = sensor_value
            units[sensor_type] = sensor_unit
            date_time_formatted = date_time.strftime("%H:%M:%S %d.%m.%Y")
            data[class_id]["time"] = date_time_formatted

    data["units"] = units

    cursor.close()
    connection.close()
    return data


if __name__ == '__main__':
    # print(type(rooms))
    # print(rooms)

    # print(type(room_details_001))
    # print(room_details_001)

    print(get_all_sensors())
