import json
import datetime
import re
import mysql.connector
import requests
import flask

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

CORS_ip = "*"
relay_ips = {
    "1": "192.168.1.151",
    "2": "192.168.1.184"
}



"""  STARY SPOSOB
room_details_001 = {"id": "room_001", "temperature": 1.0, "humidity": 135.0, "co2": 100}
room_details_002 = {"id": "room_002", "temperature": 2.0, "humidity": 22.0, "co2": 200}
room_details_003 = {"id": "room_003", "temperature": 3.0, "humidity": 522.0, "co2": 400}
rooms = [room_details_001, room_details_002, room_details_003]
"""


def cant_connect_to_aquarium(response: flask.Response):
    response.data = """{"error":"Cannot connect to aquarium"}"""
    response.status_code = 503
    return response

units = {}


def get_all_sensors():
    connection = mysql.connector.connect(host=DATABASE_HOST,
                                         database=DATABASE_NAME,
                                         user=DATABASE_USER,
                                         password=DATABASE_PASSWORD, port=DATABASE_PORT)
    # connection = mysql.connector.connect(host="localhost",
    #                                      database=L_DATABASE_NAME,
    #                                      user=L_DATABASE_USER,
    #                                      password=L_DATABASE_PASSWORD)
    cursor = connection.cursor()

    """ AK BY SENZORY POSIELALI V CASE (limitne) BLIZIACOM SA datetime A POSIEALI BY VSETKY
    cursor.execute("SELECT `room_number`, `sensor_type`,
                    `sensor_value`, `sensor_unit` FROM `rooms` r WHERE r.`date_time` ="
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


def get_sensors_aquarium():
    r = requests.Response
    response = flask.Response()
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = CORS_ip
    try:
        r = requests.get("http://" + relay_ips.get("1") + "/cm?cmnd=status%2010", timeout=5)
        r2 = requests.get("http://" + relay_ips.get("2") + "/cm?cmnd=status%2010", timeout=5)
    except requests.exceptions.ConnectionError:
        return cant_connect_to_aquarium(response)
    else:
        response_text = {}
        r_json = json.loads(r.text)
        r2_json = json.loads(r2.text)
        date_time = datetime.datetime.strptime(r_json["StatusSNS"]["Time"], "%Y-%m-%dT%H:%M:%S")
        date_time = date_time.replace(
            day=(date_time.day + ((date_time.hour + 1) // 24)),
            hour=(date_time.hour + 1) % 24
        )

        response_text["date"] = date_time.strftime("%d.%m.%Y")
        response_text["time"] = date_time.strftime("%H:%M:%S")
        response_text["w_temp"] = r_json["StatusSNS"]["DHT11"]["Temperature"]
        response_text["a_temp"] = r2_json["StatusSNS"]["DHT11"]["Temperature"]
        response_text["a_hum"] = r2_json["StatusSNS"]["DHT11"]["Humidity"]
        response_text["temp_unit"] = r_json["StatusSNS"]["TempUnit"]
        response.data = json.dumps(response_text)
        response.status_code = 200
        return response


def toggle_relay(relay_id, to_state=None):
    response = flask.Response()
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = CORS_ip
    ip = None

    if relay_id not in {"1", "2"}:
        response.data = '{"error":"Wrong relay ID"}'
        response.status_code = 404
        return response
    ip = relay_ips.get(relay_id)

    r = requests.Response

    try:
        if not to_state:
            r = requests.get("http://" + ip + "/cm?cmnd=Power%20TOGGLE", timeout=0.5)
        else:
            request = "http://" + ip + "/cm?cmnd=Power%20" + to_state if to_state in ("On", "Off") else "http://" + ip + "/cm?cmnd=Power"
            r = requests.get(request, timeout=0.5)
    except requests.exceptions.ConnectionError:
        return cant_connect_to_aquarium(response)
    else:
        response.data = r.text
        response.status_code = 200
        return response


if __name__ == '__main__':
    # print(type(rooms))
    # print(rooms)

    # print(type(room_details_001))
    # print(room_details_001)

    print(get_all_sensors())
