from flask import Blueprint, Response, session, render_template
import time
import os
import sys

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join(script_dir, '..', "..")
sys.path.append(mymodule_dir)

import smartschool.app.modules.sensor_details as sensor_details


sensors_response_cache = Response
last_sensors_request = 0
relay_response_cache = Response
last_relay_request = 0

aquarium_api = Blueprint('aquarium_api', __name__)


@aquarium_api.route("/aquarium", methods=["GET"])
def show_aquarium():
    if not session.get("is_admin"):
        return render_template("/aquarium.html", without=True)

    if not session["is_admin"]:
        return render_template("/aquarium.html", without=True)

    return render_template("/aquarium.html", without=False)


@aquarium_api.route('/aquarium/api/get_sensors_aquarium')
def retrieve_all_data_from_aquarium_sensors():
    global last_sensors_request, sensors_response_cache
    if int(time.time() * 1000) - last_sensors_request < 250:
        print("CACHED:", sensors_response_cache.data)
        return sensors_response_cache
    last_sensors_request = int(time.time() * 1000)
    response = sensor_details.get_sensors_aquarium()
    sensors_response_cache = response
    print(response.data)
    """

    resp = Response(json.dumps({"date": "2021-05-10",
                                "time": "18:31:10",
                                "w_temp": 22.9,
                                "a_temp": 23.0,
                                "a_hum": 39.0,
                                "temp_unit": "C"}))
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp"""
    return response


@aquarium_api.route('/aquarium/api/relay/<relay_id>/toggle/')
@aquarium_api.route('/aquarium/api/relay/<relay_id>/toggle/<state>/')
def toggle_relay(relay_id, state=None):
    if not session.get("is_admin"):
        return "", 401
    """
    global last_relay_request, relay_response_cache
    if int(time.time() * 1000) - last_relay_request < 500:
        print("CACHED:", relay_response_cache.data)
        if state:
            return relay_response_cache
        return "", 200

    last_relay_request = int(time.time() * 1000)
    """
    response = sensor_details.toggle_relay(relay_id, state)
    relay_response_cache = response
    print(response.data)

    return response


@aquarium_api.route('/aquarium/api/feed/<rotates_count>/')
# @app.route('/api/feed/')
def feed(rotates_count=1):
    if not session.get("is_admin"):
        return "", 401

    try:
        rotates_count = int(rotates_count)

    except Exception as e:
        return "", 401

    rotates_count = 5 if rotates_count > 5 else rotates_count
    rotates_count = 0 if rotates_count < 0 else rotates_count

    response = sensor_details.feed(rotates_count)
    print(response.data)

    return response
