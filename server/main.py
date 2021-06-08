import datetime
from flask import Flask, jsonify, session, Response
from flask_session import Session
import sensor_details
import mainData
import json
import time

# SESSION_COOKIE_SECURE = True
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

sensors_response_cache = Response
last_sensors_request = 0
relay_response_cache = Response
last_relay_request = 0

CORS_ip = "*"


@app.route('/api/')
def hello():
    session['count'] = 0
    return "Ahoj svet!\n"


@app.route('/api/get_sensors')
def retrieve_all_data_from_all_sensors():
    result = sensor_details.get_all_sensors()
    resp = Response(json.dumps(result))
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"
    print(result)
    print(resp)
    return resp


@app.route('/api/ResetDate')
def reset_date():
    session["count"] = 0
    session["today"] = datetime.date.today()
    # session['today'] = mainData.smartSchool.createDate('2021', '04', '28', 'x')
    return "", 200


@app.route('/api/Candle/')
@app.route('/api/Candle/<idClass>/')
def filter_data_to_candle(idClass=None):
    print(idClass)

    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days

    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_filter = mainData.smartSchool.eliminateNoise(temp_today)

    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_filter = mainData.smartSchool.eliminateNoise(humid_today)

    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    dp_filter = mainData.smartSchool.eliminateNoise(dp_today)

    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)
    co2_filter = mainData.smartSchool.eliminateNoise(co2_volt)

    temp_candle = mainData.smartSchool.parseCandle(temp_filter)
    humid_candle = mainData.smartSchool.parseCandle(humid_filter)
    dp_candle = mainData.smartSchool.parseCandle(dp_filter)
    co2_candle = mainData.smartSchool.parseCandle(co2_filter)

    result = [[temp_candle, humid_candle, dp_candle, co2_candle],
              myDate.strftime("%a, %d %b %Y %H:%M:%S")]

    print(result)
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/CandleSub/')
@app.route('/api/CandleSub/<idClass>/')
def sub_candle(idClass=None):
    session["count"] -= 1
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days

    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_filter = mainData.smartSchool.eliminateNoise(temp_today)

    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_filter = mainData.smartSchool.eliminateNoise(humid_today)

    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    dp_filter = mainData.smartSchool.eliminateNoise(dp_today)

    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)
    co2_filter = mainData.smartSchool.eliminateNoise(co2_volt)

    temp_candle = mainData.smartSchool.parseCandle(temp_filter)
    humid_candle = mainData.smartSchool.parseCandle(humid_filter)
    dp_candle = mainData.smartSchool.parseCandle(dp_filter)
    co2_candle = mainData.smartSchool.parseCandle(co2_filter)

    result = [[temp_candle, humid_candle, dp_candle, co2_candle],
              myDate.strftime("%a, %d %b %Y %H:%M:%S")]

    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/CandleAdd/<idClass>/')
@app.route('/api/CandleAdd/')
def add_candle(idClass=None):
    session["count"] += 1
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days

    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_filter = mainData.smartSchool.eliminateNoise(temp_today)

    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_filter = mainData.smartSchool.eliminateNoise(humid_today)

    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    dp_filter = mainData.smartSchool.eliminateNoise(dp_today)

    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)
    co2_filter = mainData.smartSchool.eliminateNoise(co2_volt)

    temp_candle = mainData.smartSchool.parseCandle(temp_filter)
    humid_candle = mainData.smartSchool.parseCandle(humid_filter)
    dp_candle = mainData.smartSchool.parseCandle(dp_filter)
    co2_candle = mainData.smartSchool.parseCandle(co2_filter)

    result = [[temp_candle, humid_candle, dp_candle, co2_candle],
              myDate.strftime("%a, %d %b %Y %H:%M:%S")]

    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/Line/<idClass>/')
@app.route('/api/Line/')
def filter_data_to_line(idClass=None):
    print(idClass)
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days
    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_filter = mainData.smartSchool.eliminateNoise(temp_today)
    temp_ma = mainData.smartSchool.movingAvg(temp_filter)

    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_filter = mainData.smartSchool.eliminateNoise(humid_today)
    humid_ma = mainData.smartSchool.movingAvg(humid_filter)

    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    dp_filter = mainData.smartSchool.eliminateNoise(dp_today)
    dp_ma = mainData.smartSchool.movingAvg(dp_filter)

    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)
    co2_filter = mainData.smartSchool.eliminateNoise(co2_volt)
    co2_ma = mainData.smartSchool.movingAvg(co2_filter)

    temp_line = mainData.smartSchool.parsePlot(temp_ma)
    humid_line = mainData.smartSchool.parsePlot(humid_ma)
    dp_line = mainData.smartSchool.parsePlot(dp_ma)
    co2_line = mainData.smartSchool.parsePlot(co2_ma)

    temp_s = mainData.smartSchool.sigma(temp_today)
    humid_s = mainData.smartSchool.sigma(humid_today)
    dp_s = mainData.smartSchool.sigma(dp_today)
    co2_s = mainData.smartSchool.sigma(co2_volt)

    result = [[temp_line, humid_line, dp_line, co2_line],
              myDate.strftime("%a, %d %b %Y %H:%M:%S"),
              [temp_s, humid_s, dp_s, co2_s]
              ]
    print('RESULT')
    print(result)
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/LineSub/<idClass>/')
@app.route('/api/LineSub/')
def line_sub(idClass=None):
    session["count"] -= 1
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days

    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_filter = mainData.smartSchool.eliminateNoise(temp_today)
    temp_ma = mainData.smartSchool.movingAvg(temp_filter)

    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_filter = mainData.smartSchool.eliminateNoise(humid_today)
    humid_ma = mainData.smartSchool.movingAvg(humid_filter)

    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    dp_filter = mainData.smartSchool.eliminateNoise(dp_today)
    dp_ma = mainData.smartSchool.movingAvg(dp_filter)

    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)
    co2_filter = mainData.smartSchool.eliminateNoise(co2_volt)
    co2_ma = mainData.smartSchool.movingAvg(co2_filter)

    temp_line = mainData.smartSchool.parsePlot(temp_ma)
    humid_line = mainData.smartSchool.parsePlot(humid_ma)
    dp_line = mainData.smartSchool.parsePlot(dp_ma)
    co2_line = mainData.smartSchool.parsePlot(co2_ma)

    temp_s = mainData.smartSchool.sigma(temp_today)
    humid_s = mainData.smartSchool.sigma(humid_today)
    dp_s = mainData.smartSchool.sigma(dp_today)
    co2_s = mainData.smartSchool.sigma(co2_volt)

    result = [[temp_line, humid_line, dp_line, co2_line],
              myDate.strftime("%a, %d %b %Y %H:%M:%S"),
              [temp_s, humid_s, dp_s, co2_s]
              ]

    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/LineAdd/<idClass>/')
@app.route('/api/LineAdd/')
def line_add(idClass=None):
    session["count"] += 1
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days

    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_filter = mainData.smartSchool.eliminateNoise(temp_today)
    temp_ma = mainData.smartSchool.movingAvg(temp_filter)

    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_filter = mainData.smartSchool.eliminateNoise(humid_today)
    humid_ma = mainData.smartSchool.movingAvg(humid_filter)

    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    dp_filter = mainData.smartSchool.eliminateNoise(dp_today)
    dp_ma = mainData.smartSchool.movingAvg(dp_filter)

    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)
    co2_filter = mainData.smartSchool.eliminateNoise(co2_volt)
    co2_ma = mainData.smartSchool.movingAvg(co2_filter)

    temp_line = mainData.smartSchool.parsePlot(temp_ma)
    humid_line = mainData.smartSchool.parsePlot(humid_ma)
    dp_line = mainData.smartSchool.parsePlot(dp_ma)
    co2_line = mainData.smartSchool.parsePlot(co2_ma)

    temp_s = mainData.smartSchool.sigma(temp_today)
    humid_s = mainData.smartSchool.sigma(humid_today)
    dp_s = mainData.smartSchool.sigma(dp_today)
    co2_s = mainData.smartSchool.sigma(co2_volt)

    result = [[temp_line, humid_line, dp_line, co2_line],
              myDate.strftime("%a, %d %b %Y %H:%M:%S"),
              [temp_s, humid_s, dp_s, co2_s]
              ]

    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/get_sensors_aquarium')
def retrieve_all_data_from_aquarium_sensors():
    global last_sensors_request, sensors_response_cache
    if int(time.time() * 1000) - last_sensors_request < 250:
        print("CACHED:", sensors_response_cache.data)
        return sensors_response_cache
    last_sensors_request = int(time.time() * 1000)
    response = sensor_details.get_sensors_aquarium()
    sensors_response_cache = response
    print(response.data)

    """resp = Response(json.dumps({"StatusSNS": {"Time": "2021-05-10T10:59:18",
                                              "SI7021": {"Temperature": 26.3, "Humidity": 43.2, "DewPoint": 12.8},
                                              "TempUnit": "C"}}))
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp"""
    return response


@app.route('/api/relay/<relay_id>/toggle/')
@app.route('/api/relay/<relay_id>/toggle/<state>/')
def toggle_relay(relay_id, state=None):
    global last_relay_request, relay_response_cache
    if int(time.time() * 1000) - last_relay_request < 500:
        print("CACHED:", relay_response_cache.data)
        if state:
            return relay_response_cache
        return "", 200
    last_relay_request = int(time.time() * 1000)
    response = sensor_details.toggle_relay(relay_id, state)
    relay_response_cache = response
    print(response.data)

    return response


if __name__ == '__main__':
    # app.run(host="192.168.25.104")
    app.run(debug=True)
