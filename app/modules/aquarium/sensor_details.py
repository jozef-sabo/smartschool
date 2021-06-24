import json
import datetime
import requests
import flask

# SECRETS IMPORT
L_DB_config = {}
config = {}

try:
    from secrets import *
except ImportError:
    pass

CORS_ip = "*"
relay_ips = {
    "1": "10.0.5.111",
    "2": "10.0.5.25"
}
motor_ip = "10.0.4.130"


def cant_connect_to_aquarium(response: flask.Response):
    response.data = """{"error":"Cannot connect to aquarium"}"""
    response.status_code = 503
    return response


def get_sensors_aquarium():
    r = requests.Response
    response = flask.Response()
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = CORS_ip
    try:
        r = requests.get("http://" + relay_ips.get("1") + "", timeout=10)
        r2 = requests.get("http://" + relay_ips.get("2") + "/cm?cmnd=status%2010", timeout=10)
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
        response_text["w_temp"] = r_json["StatusSNS"]["DS18B20"]["Temperature"]
        response_text["a_temp"] = r2_json["StatusSNS"]["SI7021"]["Temperature"]
        response_text["a_hum"] = r2_json["StatusSNS"]["SI7021"]["Humidity"]
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
            r = requests.get("http://" + ip + "/cm?cmnd=Power%20TOGGLE", timeout=10)
        else:
            request = "http://" + ip + "/cm?cmnd=Power%20" + to_state if to_state in ("On", "Off") else "http://" + ip + "/cm?cmnd=Power"
            r = requests.get(request, timeout=10)
    except requests.exceptions.ConnectionError:
        return cant_connect_to_aquarium(response)
    else:
        response.data = r.text
        response.status_code = 200
        return response


def feed(rotates_count):
    response = flask.Response()
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = CORS_ip

    r = requests.Response
    angle = rotates_count * 360

    try:
        r = requests.get("http://" + motor_ip + "/cm?cmnd=MotorRotate -" + str(angle), timeout=15)
    except requests.exceptions.ConnectionError:
        return cant_connect_to_aquarium(response)
    else:
        response.data = r.text
        response.status_code = 200
        return response