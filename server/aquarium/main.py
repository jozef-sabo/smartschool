from flask import Flask, jsonify, request, Response
import sensor_details
import time


app = Flask(__name__)
sensors_response_cache = Response
last_sensors_request = 0
relay_response_cache = Response
last_relay_request = 0


@app.route('/')
def hello():
    return "Ahoj svet!\n"


@app.route('/api/get_sensors')
def retrieve_all_data_from_all_sensors():
    global last_sensors_request, sensors_response_cache
    if int(time.time() * 1000) - last_sensors_request < 250:
        print("CACHED:", sensors_response_cache.data)
        return sensors_response_cache
    last_sensors_request = int(time.time() * 1000)
    response = sensor_details.get_all_sensors()
    sensors_response_cache = response
    print(response.data)

    return {"StatusSNS":{"Time":"2021-05-10T10:59:18","SI7021":{"Temperature":26.3,"Humidity":43.2,"DewPoint":12.8},"TempUnit":"C"}}
    # return response


@app.route('/api/relay/toggle/')
@app.route('/api/relay/toggle/<state>/')
def toggle_relay(state=None):
    global last_relay_request, relay_response_cache
    if int(time.time() * 1000) - last_relay_request < 500:
        print("CACHED:", relay_response_cache.data)
        if state:
            return relay_response_cache
        return "", 200
    last_relay_request = int(time.time() * 1000)
    response = sensor_details.toggle_relay(state)
    relay_response_cache = response
    print(response.data)

    return response


if __name__ == '__main__':
    # app.run(host="192.168.25.104")
    app.run(debug=True, port=8080)
