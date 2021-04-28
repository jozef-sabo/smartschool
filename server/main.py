import datetime
from flask import Flask, jsonify, session, Response
from flask_session import Session
import sensor_details
import mainData
import json


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


@app.route('/api/Candle')
def filter_data_to_candle():
    session["count"] = 0
    db_data = mainData.fetchData.fetch()

    myDate = mainData.smartSchool.createDate('2021', '04', '27', 'x')

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    # temp_today_candle = mainData.smartSchool.parseCandle(temp_today)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)
    temp_06_04_2021_candle = mainData.smartSchool.parseCandle(temp_06_04_2021)

    humid_all = mainData.smartSchool.filterByType(db_data, "Humidity")
    # humid_today = mainData.smartSchool.filterTodayData(humid_all)
    # humid_today_candle = mainData.smartSchool.parseCandle(humid_today)
    humid_06_04_2021 = mainData.smartSchool.filterByDateTime(humid_all, myDate)
    humid_06_04_2021_candle = mainData.smartSchool.parseCandle(humid_06_04_2021)

    dp_all = mainData.smartSchool.filterByType(db_data, "DewPoint")
    # dp_today = mainData.smartSchool.filterTodayData(dp_all)
    # dp_today_candle = mainData.smartSchool.parseCandle(dp_today)
    dp_06_04_2021 = mainData.smartSchool.filterByDateTime(dp_all, myDate)
    dp_06_04_2021_candle = mainData.smartSchool.parseCandle(dp_06_04_2021)

    a0_all = mainData.smartSchool.filterByType(db_data, "A0")
    # a0_today = mainData.smartSchool.filterTodayData(a0_all)
    # a0_today_candle = mainData.smartSchool.parseCandle(a0_today)
    a0_06_04_2021 = mainData.smartSchool.filterByDateTime(a0_all, myDate)
    a0_06_04_2021_volt = mainData.smartSchool.a0volt(a0_06_04_2021)
    a0_06_04_2021_candle = mainData.smartSchool.parseCandle(a0_06_04_2021_volt)

    result = [[temp_06_04_2021_candle, humid_06_04_2021_candle, dp_06_04_2021_candle, a0_06_04_2021_candle],
              myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/CandleSub')
def sub_candle():
    print("KukÃ¡me")
    print(session["count"])
    session["count"] -= 1
    print(session["count"])
    days = datetime.timedelta(session["count"])

    db_data = mainData.fetchData.fetch()

    myDate = mainData.smartSchool.createDate('2021', '04', '27', 'x') 
    myDate = myDate + days # namiesto myDate - date.today()
    print(myDate)

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    # temp_today_candle = mainData.smartSchool.parseCandle(temp_today)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)
    temp_06_04_2021_candle = mainData.smartSchool.parseCandle(temp_06_04_2021)

    humid_all = mainData.smartSchool.filterByType(db_data, "Humidity")
    # humid_today = mainData.smartSchool.filterTodayData(humid_all)
    # humid_today_candle = mainData.smartSchool.parseCandle(humid_today)
    humid_06_04_2021 = mainData.smartSchool.filterByDateTime(humid_all, myDate)
    humid_06_04_2021_candle = mainData.smartSchool.parseCandle(humid_06_04_2021)

    dp_all = mainData.smartSchool.filterByType(db_data, "DewPoint")
    # dp_today = mainData.smartSchool.filterTodayData(dp_all)
    # dp_today_candle = mainData.smartSchool.parseCandle(dp_today)
    dp_06_04_2021 = mainData.smartSchool.filterByDateTime(dp_all, myDate)
    dp_06_04_2021_candle = mainData.smartSchool.parseCandle(dp_06_04_2021)

    a0_all = mainData.smartSchool.filterByType(db_data, "A0")
    # a0_today = mainData.smartSchool.filterTodayData(a0_all)
    # a0_today_candle = mainData.smartSchool.parseCandle(a0_today)
    a0_06_04_2021 = mainData.smartSchool.filterByDateTime(a0_all, myDate)
    a0_06_04_2021_volt = mainData.smartSchool.a0volt(a0_06_04_2021)
    a0_06_04_2021_candle = mainData.smartSchool.parseCandle(a0_06_04_2021_volt)

    result = [[temp_06_04_2021_candle, humid_06_04_2021_candle, dp_06_04_2021_candle, a0_06_04_2021_candle],
              myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/CandleAdd')
def add_candle():
    session["count"] += 1
    days = datetime.timedelta(session["count"])

    db_data = mainData.fetchData.fetch()

    myDate = mainData.smartSchool.createDate('2021', '04', '27', 'x')
    myDate = myDate + days # namiesto myDate - date.today()
    print(myDate)

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    # temp_today_candle = mainData.smartSchool.parseCandle(temp_today)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)
    temp_06_04_2021_candle = mainData.smartSchool.parseCandle(temp_06_04_2021)

    humid_all = mainData.smartSchool.filterByType(db_data, "Humidity")
    # humid_today = mainData.smartSchool.filterTodayData(humid_all)
    # humid_today_candle = mainData.smartSchool.parseCandle(humid_today)
    humid_06_04_2021 = mainData.smartSchool.filterByDateTime(humid_all, myDate)
    humid_06_04_2021_candle = mainData.smartSchool.parseCandle(humid_06_04_2021)

    dp_all = mainData.smartSchool.filterByType(db_data, "DewPoint")
    # dp_today = mainData.smartSchool.filterTodayData(dp_all)
    # dp_today_candle = mainData.smartSchool.parseCandle(dp_today)
    dp_06_04_2021 = mainData.smartSchool.filterByDateTime(dp_all, myDate)
    dp_06_04_2021_candle = mainData.smartSchool.parseCandle(dp_06_04_2021)

    a0_all = mainData.smartSchool.filterByType(db_data, "A0")
    # a0_today = mainData.smartSchool.filterTodayData(a0_all)
    # a0_today_candle = mainData.smartSchool.parseCandle(a0_today)
    a0_06_04_2021 = mainData.smartSchool.filterByDateTime(a0_all, myDate)
    a0_06_04_2021_volt = mainData.smartSchool.a0volt(a0_06_04_2021)
    a0_06_04_2021_candle = mainData.smartSchool.parseCandle(a0_06_04_2021_volt)

    result = [[temp_06_04_2021_candle, humid_06_04_2021_candle, dp_06_04_2021_candle, a0_06_04_2021_candle],
              myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/Line')
def filter_data_to_line():
    session["count"] = 0

    db_data = mainData.fetchData.fetch()

    myDate = mainData.smartSchool.createDate('2021', '04', '27', 'x')

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)
    temp_06_04_2021_line = mainData.smartSchool.parsePlot(temp_06_04_2021)

    humid_all = mainData.smartSchool.filterByType(db_data, "Humidity")
    # humid_today = mainData.smartSchool.filterTodayData(humid_all)
    humid_06_04_2021 = mainData.smartSchool.filterByDateTime(humid_all, myDate)
    humid_06_04_2021_line = mainData.smartSchool.parsePlot(humid_06_04_2021)

    dp_all = mainData.smartSchool.filterByType(db_data, "DewPoint")
    # dp_today = mainData.smartSchool.filterTodayData(dp_all)
    dp_06_04_2021 = mainData.smartSchool.filterByDateTime(dp_all, myDate)
    dp_06_04_2021_line = mainData.smartSchool.parsePlot(dp_06_04_2021)

    a0_all = mainData.smartSchool.filterByType(db_data, "A0")
    # a0_today = mainData.smartSchool.filterTodayData(a0_all)
    a0_06_04_2021 = mainData.smartSchool.filterByDateTime(a0_all, myDate)
    a0_06_04_2021_volt = mainData.smartSchool.a0volt(a0_06_04_2021)
    a0_06_04_2021_line = mainData.smartSchool.parsePlot(a0_06_04_2021_volt)

    temp_av = mainData.smartSchool.avg(temp_06_04_2021_line)
    humid_av = mainData.smartSchool.avg(humid_06_04_2021_line)
    dp_av = mainData.smartSchool.avg(dp_06_04_2021_line)
    a0_av = mainData.smartSchool.avg(a0_06_04_2021_line)

    result = [[temp_06_04_2021_line.tolist(), humid_06_04_2021_line.tolist(), dp_06_04_2021_line.tolist(),
               a0_06_04_2021_line.tolist()], [temp_av, humid_av, dp_av, a0_av], myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/LineSub')
def line_sub():
    session["count"] -= 1
    days = datetime.timedelta(session["count"])

    myDate = mainData.smartSchool.createDate('2021', '04', '27', 'x')
    myDate = myDate + days # namiesto myDate - date.today()
    print(myDate)

    db_data = mainData.fetchData.fetch()

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)
    temp_06_04_2021_line = mainData.smartSchool.parsePlot(temp_06_04_2021)

    humid_all = mainData.smartSchool.filterByType(db_data, "Humidity")
    # humid_today = mainData.smartSchool.filterTodayData(humid_all)
    humid_06_04_2021 = mainData.smartSchool.filterByDateTime(humid_all, myDate)
    humid_06_04_2021_line = mainData.smartSchool.parsePlot(humid_06_04_2021)

    dp_all = mainData.smartSchool.filterByType(db_data, "DewPoint")
    # dp_today = mainData.smartSchool.filterTodayData(dp_all)
    dp_06_04_2021 = mainData.smartSchool.filterByDateTime(dp_all, myDate)
    dp_06_04_2021_line = mainData.smartSchool.parsePlot(dp_06_04_2021)

    a0_all = mainData.smartSchool.filterByType(db_data, "A0")
    # a0_today = mainData.smartSchool.filterTodayData(a0_all)
    a0_06_04_2021 = mainData.smartSchool.filterByDateTime(a0_all, myDate)
    a0_06_04_2021_volt = mainData.smartSchool.a0volt(a0_06_04_2021)
    a0_06_04_2021_line = mainData.smartSchool.parsePlot(a0_06_04_2021_volt)

    temp_av = mainData.smartSchool.avg(temp_06_04_2021_line)
    humid_av = mainData.smartSchool.avg(humid_06_04_2021_line)
    dp_av = mainData.smartSchool.avg(dp_06_04_2021_line)
    a0_av = mainData.smartSchool.avg(a0_06_04_2021_line)

    result = [[temp_06_04_2021_line.tolist(), humid_06_04_2021_line.tolist(), dp_06_04_2021_line.tolist(),
               a0_06_04_2021_line.tolist()],[temp_av, humid_av, dp_av, a0_av], myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


@app.route('/api/LineAdd')
def line_add():
    session["count"] += 1
    days = datetime.timedelta(session["count"])

    myDate = mainData.smartSchool.createDate('2021', '04', '27', 'x')
    myDate = myDate + days # namiesto myDate - date.today()
    print(myDate)

    db_data = mainData.fetchData.fetch()

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)
    temp_06_04_2021_line = mainData.smartSchool.parsePlot(temp_06_04_2021)

    humid_all = mainData.smartSchool.filterByType(db_data, "Humidity")
    # humid_today = mainData.smartSchool.filterTodayData(humid_all)
    humid_06_04_2021 = mainData.smartSchool.filterByDateTime(humid_all, myDate)
    humid_06_04_2021_line = mainData.smartSchool.parsePlot(humid_06_04_2021)

    dp_all = mainData.smartSchool.filterByType(db_data, "DewPoint")
    # dp_today = mainData.smartSchool.filterTodayData(dp_all)
    dp_06_04_2021 = mainData.smartSchool.filterByDateTime(dp_all, myDate)
    dp_06_04_2021_line = mainData.smartSchool.parsePlot(dp_06_04_2021)

    a0_all = mainData.smartSchool.filterByType(db_data, "A0")
    # a0_today = mainData.smartSchool.filterTodayData(a0_all)
    a0_06_04_2021 = mainData.smartSchool.filterByDateTime(a0_all, myDate)
    a0_06_04_2021_volt = mainData.smartSchool.a0volt(a0_06_04_2021)
    a0_06_04_2021_line = mainData.smartSchool.parsePlot(a0_06_04_2021_volt)

    temp_av = mainData.smartSchool.avg(temp_06_04_2021_line)
    humid_av = mainData.smartSchool.avg(humid_06_04_2021_line)
    dp_av = mainData.smartSchool.avg(dp_06_04_2021_line)
    a0_av = mainData.smartSchool.avg(a0_06_04_2021_line)

    result = [[temp_06_04_2021_line.tolist(), humid_06_04_2021_line.tolist(), dp_06_04_2021_line.tolist(),
               a0_06_04_2021_line.tolist()],[temp_av, humid_av, dp_av, a0_av], myDate.strftime("%a, %d %b %Y %H:%M:%S")]
    result_json = json.dumps(result)

    resp = Response(result_json)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = "application/json"

    return resp


if __name__ == '__main__':
    #app.run(host="192.168.25.104")
    app.run(debug=True)
