from flask import Blueprint, Response, session
import os
import sys
import datetime
import json

script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join(script_dir, '..', "..")
sys.path.append(mymodule_dir)

import smartschool.app.modules.sensor_details as sensor_details
import smartschool.app.modules.smartSchool as smartSchool
import smartschool.app.modules.fetchData as fetchData

smartschool = Blueprint('smartschool', __name__)

CORS_ip = "*"


@smartschool.route('/api/')
def hello():
    session['count'] = 0
    return "Ahoj svet!\n"


@smartschool.route('/api/get_sensors')
def retrieve_all_data_from_all_sensors():
    result = sensor_details.get_all_sensors()
    resp = Response(json.dumps(result))
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"
    print(result)
    print(resp)
    return resp


@smartschool.route('/api/ResetDate')
def reset_date():
    session["count"] = 0
    session["today"] = datetime.date.today()
    # session['today'] = smartSchool.createDate('2021', '04', '28', 'x')
    return "", 200


@smartschool.route('/api/Candle/')
@smartschool.route('/api/Candle/<id_class>/')
def filter_data_to_candle(id_class=None):
    print(id_class)

    days = datetime.timedelta(session["count"])
    my_date = session["today"] + days

    temp_today = fetchData.fetch(my_date, id_class, 'temperature')
    temp_filter = smartSchool.eliminateNoise(temp_today)

    humid_today = fetchData.fetch(my_date, id_class, 'humidity')
    humid_filter = smartSchool.eliminateNoise(humid_today)

    dp_today = fetchData.fetch(my_date, id_class, 'dew_point')
    dp_filter = smartSchool.eliminateNoise(dp_today)

    co2_today = fetchData.fetch(my_date, id_class, 'co2')
    co2_volt = smartSchool.a0volt(co2_today)
    co2_filter = smartSchool.eliminateNoise(co2_volt)

    temp_candle = smartSchool.parseCandle(temp_filter)
    humid_candle = smartSchool.parseCandle(humid_filter)
    dp_candle = smartSchool.parseCandle(dp_filter)
    co2_candle = smartSchool.parseCandle(co2_filter)

    result = [[temp_candle, humid_candle, dp_candle, co2_candle],
              my_date.strftime("%a, %d %b %Y %H:%M:%S")]

    print(result)
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@smartschool.route('/api/CandleSub/')
@smartschool.route('/api/CandleSub/<id_class>/')
def sub_candle(id_class=None):
    session["count"] -= 1
    days = datetime.timedelta(session["count"])
    my_date = session["today"] + days

    temp_today = fetchData.fetch(my_date, id_class, 'temperature')
    temp_filter = smartSchool.eliminateNoise(temp_today)

    humid_today = fetchData.fetch(my_date, id_class, 'humidity')
    humid_filter = smartSchool.eliminateNoise(humid_today)

    dp_today = fetchData.fetch(my_date, id_class, 'dew_point')
    dp_filter = smartSchool.eliminateNoise(dp_today)

    co2_today = fetchData.fetch(my_date, id_class, 'co2')
    co2_volt = smartSchool.a0volt(co2_today)
    co2_filter = smartSchool.eliminateNoise(co2_volt)

    temp_candle = smartSchool.parseCandle(temp_filter)
    humid_candle = smartSchool.parseCandle(humid_filter)
    dp_candle = smartSchool.parseCandle(dp_filter)
    co2_candle = smartSchool.parseCandle(co2_filter)

    result = [[temp_candle, humid_candle, dp_candle, co2_candle],
              my_date.strftime("%a, %d %b %Y %H:%M:%S")]

    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@smartschool.route('/api/CandleAdd/<id_class>/')
@smartschool.route('/api/CandleAdd/')
def add_candle(id_class=None):
    session["count"] += 1
    days = datetime.timedelta(session["count"])
    my_date = session["today"] + days

    temp_today = fetchData.fetch(my_date, id_class, 'temperature')
    temp_filter = smartSchool.eliminateNoise(temp_today)

    humid_today = fetchData.fetch(my_date, id_class, 'humidity')
    humid_filter = smartSchool.eliminateNoise(humid_today)

    dp_today = fetchData.fetch(my_date, id_class, 'dew_point')
    dp_filter = smartSchool.eliminateNoise(dp_today)

    co2_today = fetchData.fetch(my_date, id_class, 'co2')
    co2_volt = smartSchool.a0volt(co2_today)
    co2_filter = smartSchool.eliminateNoise(co2_volt)

    temp_candle = smartSchool.parseCandle(temp_filter)
    humid_candle = smartSchool.parseCandle(humid_filter)
    dp_candle = smartSchool.parseCandle(dp_filter)
    co2_candle = smartSchool.parseCandle(co2_filter)

    result = [[temp_candle, humid_candle, dp_candle, co2_candle],
              my_date.strftime("%a, %d %b %Y %H:%M:%S")]

    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@smartschool.route('/api/Line/<id_class>/')
@smartschool.route('/api/Line/')
def filter_data_to_line(id_class=None):
    print(id_class)
    days = datetime.timedelta(session["count"])
    my_date = session["today"] + days
    temp_today = fetchData.fetch(my_date, id_class, 'temperature')
    temp_filter = smartSchool.eliminateNoise(temp_today)
    temp_ma = smartSchool.movingAvg(temp_filter)

    humid_today = fetchData.fetch(my_date, id_class, 'humidity')
    humid_filter = smartSchool.eliminateNoise(humid_today)
    humid_ma = smartSchool.movingAvg(humid_filter)

    dp_today = fetchData.fetch(my_date, id_class, 'dew_point')
    dp_filter = smartSchool.eliminateNoise(dp_today)
    dp_ma = smartSchool.movingAvg(dp_filter)

    co2_today = fetchData.fetch(my_date, id_class, 'co2')
    co2_volt = smartSchool.a0volt(co2_today)
    co2_filter = smartSchool.eliminateNoise(co2_volt)
    co2_ma = smartSchool.movingAvg(co2_filter)

    temp_line = smartSchool.parsePlot(temp_ma)
    humid_line = smartSchool.parsePlot(humid_ma)
    dp_line = smartSchool.parsePlot(dp_ma)
    co2_line = smartSchool.parsePlot(co2_ma)

    temp_s = smartSchool.sigma(temp_today)
    humid_s = smartSchool.sigma(humid_today)
    dp_s = smartSchool.sigma(dp_today)
    co2_s = smartSchool.sigma(co2_volt)

    result = [[temp_line, humid_line, dp_line, co2_line],
              my_date.strftime("%a, %d %b %Y %H:%M:%S"),
              [temp_s, humid_s, dp_s, co2_s]
              ]
    print('RESULT')
    print(result)
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@smartschool.route('/api/LineSub/<id_class>/')
@smartschool.route('/api/LineSub/')
def line_sub(id_class=None):
    session["count"] -= 1
    days = datetime.timedelta(session["count"])
    my_date = session["today"] + days

    temp_today = fetchData.fetch(my_date, id_class, 'temperature')
    temp_filter = smartSchool.eliminateNoise(temp_today)
    temp_ma = smartSchool.movingAvg(temp_filter)

    humid_today = fetchData.fetch(my_date, id_class, 'humidity')
    humid_filter = smartSchool.eliminateNoise(humid_today)
    humid_ma = smartSchool.movingAvg(humid_filter)

    dp_today = fetchData.fetch(my_date, id_class, 'dew_point')
    dp_filter = smartSchool.eliminateNoise(dp_today)
    dp_ma = smartSchool.movingAvg(dp_filter)

    co2_today = fetchData.fetch(my_date, id_class, 'co2')
    co2_volt = smartSchool.a0volt(co2_today)
    co2_filter = smartSchool.eliminateNoise(co2_volt)
    co2_ma = smartSchool.movingAvg(co2_filter)

    temp_line = smartSchool.parsePlot(temp_ma)
    humid_line = smartSchool.parsePlot(humid_ma)
    dp_line = smartSchool.parsePlot(dp_ma)
    co2_line = smartSchool.parsePlot(co2_ma)

    temp_s = smartSchool.sigma(temp_today)
    humid_s = smartSchool.sigma(humid_today)
    dp_s = smartSchool.sigma(dp_today)
    co2_s = smartSchool.sigma(co2_volt)

    result = [[temp_line, humid_line, dp_line, co2_line],
              my_date.strftime("%a, %d %b %Y %H:%M:%S"),
              [temp_s, humid_s, dp_s, co2_s]
              ]

    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp


@smartschool.route('/api/LineAdd/<id_class>/')
@smartschool.route('/api/LineAdd/')
def line_add(id_class=None):
    session["count"] += 1
    days = datetime.timedelta(session["count"])
    my_date = session["today"] + days

    temp_today = fetchData.fetch(my_date, id_class, 'temperature')
    temp_filter = smartSchool.eliminateNoise(temp_today)
    temp_ma = smartSchool.movingAvg(temp_filter)

    humid_today = fetchData.fetch(my_date, id_class, 'humidity')
    humid_filter = smartSchool.eliminateNoise(humid_today)
    humid_ma = smartSchool.movingAvg(humid_filter)

    dp_today = fetchData.fetch(my_date, id_class, 'dew_point')
    dp_filter = smartSchool.eliminateNoise(dp_today)
    dp_ma = smartSchool.movingAvg(dp_filter)

    co2_today = fetchData.fetch(my_date, id_class, 'co2')
    co2_volt = smartSchool.a0volt(co2_today)
    co2_filter = smartSchool.eliminateNoise(co2_volt)
    co2_ma = smartSchool.movingAvg(co2_filter)

    temp_line = smartSchool.parsePlot(temp_ma)
    humid_line = smartSchool.parsePlot(humid_ma)
    dp_line = smartSchool.parsePlot(dp_ma)
    co2_line = smartSchool.parsePlot(co2_ma)

    temp_s = smartSchool.sigma(temp_today)
    humid_s = smartSchool.sigma(humid_today)
    dp_s = smartSchool.sigma(dp_today)
    co2_s = smartSchool.sigma(co2_volt)

    result = [[temp_line, humid_line, dp_line, co2_line],
              my_date.strftime("%a, %d %b %Y %H:%M:%S"),
              [temp_s, humid_s, dp_s, co2_s]
              ]

    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp