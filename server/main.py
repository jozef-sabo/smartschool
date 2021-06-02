import datetime
import json
import time
from flask import Flask, session, Response, request, render_template
from flask_session import Session
import sensor_details
import smartSchool
import fetchData
import login

# SESSION_COOKIE_SECURE = True
app = Flask(__name__, template_folder="static/web")
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
    # session['today'] = smartSchool.createDate('2021', '04', '28', 'x')
    return "", 200


@app.route('/api/Candle/')
@app.route('/api/Candle/<id_class>/')
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


@app.route('/api/CandleSub/')
@app.route('/api/CandleSub/<id_class>/')
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


@app.route('/api/CandleAdd/<id_class>/')
@app.route('/api/CandleAdd/')
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


@app.route('/api/Line/<id_class>/')
@app.route('/api/Line/')
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


@app.route('/api/LineSub/<id_class>/')
@app.route('/api/LineSub/')
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


@app.route('/api/LineAdd/<id_class>/')
@app.route('/api/LineAdd/')
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


@app.route('/api/get_sensors_aquarium')
def retrieve_all_data_from_aquarium_sensors():
    """global last_sensors_request, sensors_response_cache
    if int(time.time() * 1000) - last_sensors_request < 250:
        print("CACHED:", sensors_response_cache.data)
        return sensors_response_cache
    last_sensors_request = int(time.time() * 1000)
    response = sensor_details.get_sensors_aquarium()
    sensors_response_cache = response
    print(response.data)"""

    resp = Response(json.dumps({"date": "2021-05-10",
                                "time": "18:31:10",
                                "w_temp": 22.9,
                                "a_temp": 23.0,
                                "a_hum": 39.0,
                                "temp_unit": "C"}))
    resp.headers['Access-Control-Allow-Origin'] = CORS_ip
    resp.headers['Content-Type'] = "application/json"

    return resp
    # return response


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


@app.route('/login', methods=['POST'])
def login_post():
    if not session.get("is_admin"):
        session["is_admin"] = login.login(request.form)

    resp = Response("")
    resp.headers["Location"] = "aquarium"
    resp.status_code = 302
    return resp


@app.route('/login', methods=['GET'])
def login_get():
    if not session.get("is_admin"):
        return render_template("/login.html")

    resp = Response("")
    resp.headers["Location"] = "aquarium"
    resp.status_code = 302
    return resp


@app.route('/logout')
def logout():
    if session.get("is_admin"):
        session.pop("is_admin")

    resp = Response("")
    resp.headers["Location"] = "aquarium"
    resp.status_code = 302
    return resp


@app.route("/aquarium", methods=["GET"])
def show_aquarium():
    if not session.get("is_admin"):
        return render_template("/aquarium.html")

    if not session["is_admin"]:
        return render_template("/aquarium.html")

    return render_template("/aquarium_adm.html")


if __name__ == '__main__':
    # app.run(host="192.168.25.104")
    # app.run(host="10.0.7.174", debug=True)
    app.run(host="10.0.7.59", debug=True)
