import datetime
from flask import Flask, jsonify, session, Response
from flask_session import Session
import sensor_details
import mainData
import json

# SESSION_COOKIE_SECURE = True
app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/api/')
def hello():
    session['count'] = 0
    return "Ahoj svet!\n"


@app.route('/api/get_sensors')
def retrieve_all_data_from_all_sensors():
    result = sensor_details.get_all_sensors()
    resp = Response(json.dumps(result))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"
    print(result)
    print(resp)
    return resp


@app.route('/api/ResetDate')
def reset():
    session["count"] = 0
    session["today"] = datetime.date.today()
    # session['today'] = mainData.smartSchool.createDate('2021', '04', '28', 'x')
    return "",200


@app.route('/api/Candle/')
@app.route('/api/Candle/<idClass>/')
def filter_data_to_candle(idClass=None):
    print(idClass)

    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days 
    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_today = mainData.smartSchool.filter0(temp_today)
    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_today = mainData.smartSchool.filter0(humid_today)
    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)
    print('hello')
    print(idClass)

    temp_candle = mainData.smartSchool.parseCandle(temp_today)
    humid_candle = mainData.smartSchool.parseCandle(humid_today)
    dp_candle = mainData.smartSchool.parseCandle(dp_today)
    co2_candle = mainData.smartSchool.parseCandle(co2_volt)

    result = [[temp_candle, humid_candle, dp_candle, co2_candle],
              myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    print(result)
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp



@app.route('/api/CandleSub/')
@app.route('/api/CandleSub/<idClass>/')
def sub_candle(idClass=None):
    session["count"] -= 1
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days 
    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_today = mainData.smartSchool.filter0(temp_today)
    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_today = mainData.smartSchool.filter0(humid_today)
    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)
    print(myDate, idClass)
    print(temp_today)

    temp_candle = mainData.smartSchool.parseCandle(temp_today)
    humid_candle = mainData.smartSchool.parseCandle(humid_today)
    dp_candle = mainData.smartSchool.parseCandle(dp_today)
    co2_candle = mainData.smartSchool.parseCandle(co2_volt)
    print(temp_candle)

    result = [[temp_candle, humid_candle, dp_candle, co2_candle],
              myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/CandleAdd/<idClass>/')
@app.route('/api/CandleAdd/')
def add_candle(idClass=None):
    session["count"] += 1
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days 
    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_today = mainData.smartSchool.filter0(temp_today)
    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_today = mainData.smartSchool.filter0(humid_today)
    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)

    temp_candle = mainData.smartSchool.parseCandle(temp_today)
    humid_candle = mainData.smartSchool.parseCandle(humid_today)
    dp_candle = mainData.smartSchool.parseCandle(dp_today)
    co2_candle = mainData.smartSchool.parseCandle(co2_volt)

    result = [[temp_candle, humid_candle, dp_candle, co2_candle],
              myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/Line/<idClass>/')
@app.route('/api/Line/')
def filter_data_to_line(idClass=None):
    print(idClass)
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days 
    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_today = mainData.smartSchool.filter0(temp_today)
    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_today = mainData.smartSchool.filter0(humid_today)
    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)

    temp_line = mainData.smartSchool.parsePlot(temp_today)
    humid_line = mainData.smartSchool.parsePlot(humid_today)
    dp_line = mainData.smartSchool.parsePlot(dp_today)
    co2_line = mainData.smartSchool.parsePlot(co2_volt)

    temp_av = mainData.smartSchool.avg(temp_line)
    humid_av = mainData.smartSchool.avg(humid_line)
    dp_av = mainData.smartSchool.avg(dp_line)
    a0_av = mainData.smartSchool.avg(co2_line)

    result = [[temp_line, humid_line, dp_line,
               co2_line], [temp_av, humid_av, dp_av, a0_av], myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    print(result)
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/LineSub/<idClass>/')
@app.route('/api/LineSub/')
def line_sub(idClass=None):
    session["count"] -= 1
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days 
    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_today = mainData.smartSchool.filter0(temp_today)
    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_today = mainData.smartSchool.filter0(humid_today)
    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)

    temp_line = mainData.smartSchool.parsePlot(temp_today)
    humid_line = mainData.smartSchool.parsePlot(humid_today)
    dp_line = mainData.smartSchool.parsePlot(dp_today)
    co2_line = mainData.smartSchool.parsePlot(co2_volt)

    temp_av = mainData.smartSchool.avg(temp_line)
    humid_av = mainData.smartSchool.avg(humid_line)
    dp_av = mainData.smartSchool.avg(dp_line)
    a0_av = mainData.smartSchool.avg(co2_line)

    result = [[temp_line, humid_line, dp_line,
               co2_line], [temp_av, humid_av, dp_av, a0_av], myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/LineAdd/<idClass>/')
@app.route('/api/LineAdd/')
def line_add(idClass=None):
    session["count"] += 1
    days = datetime.timedelta(session["count"])
    myDate = session["today"] + days 
    temp_today = mainData.fetchData.fetch(myDate, idClass, 'temperature')
    temp_today = mainData.smartSchool.filter0(temp_today)
    humid_today = mainData.fetchData.fetch(myDate, idClass, 'humidity')
    humid_today = mainData.smartSchool.filter0(humid_today)
    dp_today = mainData.fetchData.fetch(myDate, idClass, 'dew_point')
    co2_today = mainData.fetchData.fetch(myDate, idClass, 'co2')
    co2_volt = mainData.smartSchool.a0volt(co2_today)

    temp_line = mainData.smartSchool.parsePlot(temp_today)
    humid_line = mainData.smartSchool.parsePlot(humid_today)
    dp_line = mainData.smartSchool.parsePlot(dp_today)
    co2_line = mainData.smartSchool.parsePlot(co2_volt)

    temp_av = mainData.smartSchool.avg(temp_line)
    humid_av = mainData.smartSchool.avg(humid_line)
    dp_av = mainData.smartSchool.avg(dp_line)
    a0_av = mainData.smartSchool.avg(co2_line)

    result = [[temp_line, humid_line, dp_line,
               co2_line], [temp_av, humid_av, dp_av, a0_av], myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


if __name__ == '__main__':
    #app.run(host="192.168.25.104")
    app.run(debug=True)
