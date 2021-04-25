from flask import Flask, jsonify, session
from flask_session import Session
import sensor_details
import mainData
import json
import datetime


app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@app.route('/')
def hello():
    session['count'] = 0
    return "Ahoj svet!\n"


@app.route('/get_sensors')
def retrieve_all_data_from_all_sensors():
    result = sensor_details.get_all_sensors()
    print(type(result))
    print(result)
    return jsonify(result)


@app.route('/Candle')
def filter_data_to_candle():
    session["count"] = 0
    db_data = mainData.fetchData.fetch()

    myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x')

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

    return jsonify([[temp_06_04_2021_candle, humid_06_04_2021_candle, dp_06_04_2021_candle, a0_06_04_2021_candle], myDate])

@app.route('/CandleSub')
def sub_candle():
    session["count"] -= 1
    days = datetime.timedelta(session["count"])

    db_data = mainData.fetchData.fetch()

    myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x') 
    myDate = myDate + days # namiesto myDate - date.today()
    print(myDate)

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    # temp_today_candle = mainData.smartSchool.parseCandle(temp_today)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)

    if temp_06_04_2021.size == 0:
        session["count"] += 1
        days = datetime.timedelta(session["count"])
        myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x')# namiesto myDate - date.today()
        myDate = myDate + days # namiesto myDate - date.today()
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

    return jsonify([[temp_06_04_2021_candle, humid_06_04_2021_candle, dp_06_04_2021_candle, a0_06_04_2021_candle], myDate])

@app.route('/CandleAdd')
def add_candle():
    session["count"] += 1
    days = datetime.timedelta(session["count"])

    db_data = mainData.fetchData.fetch()

    myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x') 
    myDate = myDate + days # namiesto myDate - date.today()
    print(myDate)

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    # temp_today_candle = mainData.smartSchool.parseCandle(temp_today)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)

    if temp_06_04_2021.size == 0:
        session["count"] -= 1
        days = datetime.timedelta(session["count"])
        myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x')# namiesto myDate - date.today()
        myDate = myDate + days # namiesto myDate - date.today()
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

    return jsonify([[temp_06_04_2021_candle, humid_06_04_2021_candle, dp_06_04_2021_candle, a0_06_04_2021_candle], myDate])

@app.route('/Line')
def filter_data_to_line():
    session["count"] = 0

    db_data = mainData.fetchData.fetch()

    myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x')

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

    temp_av = mainData.smartSchool.avg(temp_06_04_2021_line[1])
    humid_av = mainData.smartSchool.avg(humid_06_04_2021_line[1])
    dp_av = mainData.smartSchool.avg(dp_06_04_2021_line[1])
    a0_av = mainData.smartSchool.avg(a0_06_04_2021_line[1])

    return jsonify([[temp_06_04_2021_line.tolist(), humid_06_04_2021_line.tolist(), dp_06_04_2021_line.tolist(), a0_06_04_2021_line.tolist()],[temp_av, humid_av, dp_av, a0_av], myDate])

@app.route('/LineSub')
def line_sub():
    session["count"] -= 1
    days = datetime.timedelta(session["count"])

    myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x')
    myDate = myDate + days # namiesto myDate - date.today()
    print(myDate)

    db_data = mainData.fetchData.fetch()

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)

    if temp_06_04_2021.size == 0:
        session["count"] += 1
        days = datetime.timedelta(session["count"])
        myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x')# namiesto myDate - date.today()
        myDate = myDate + days # namiesto myDate - date.today()
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

    temp_av = mainData.smartSchool.avg(temp_06_04_2021_line[1])
    humid_av = mainData.smartSchool.avg(humid_06_04_2021_line[1])
    dp_av = mainData.smartSchool.avg(dp_06_04_2021_line[1])
    a0_av = mainData.smartSchool.avg(a0_06_04_2021_line[1])

    return jsonify([[temp_06_04_2021_line.tolist(), humid_06_04_2021_line.tolist(), dp_06_04_2021_line.tolist(), a0_06_04_2021_line.tolist()],[temp_av, humid_av, dp_av, a0_av], myDate])

@app.route('/LineAdd')
def line_add():
    session["count"] += 1
    days = datetime.timedelta(session["count"])

    myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x')
    myDate = myDate + days # namiesto myDate - date.today()
    print(myDate)

    db_data = mainData.fetchData.fetch()

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, myDate)

    if temp_06_04_2021.size == 0:
        session["count"] -= 1
        days = datetime.timedelta(session["count"])
        myDate = mainData.smartSchool.createDate('2021', '04', '12', 'x')# namiesto myDate - date.today()
        myDate = myDate + days # namiesto myDate - date.today()
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

    temp_av = mainData.smartSchool.avg(temp_06_04_2021_line[1])
    humid_av = mainData.smartSchool.avg(humid_06_04_2021_line[1])
    dp_av = mainData.smartSchool.avg(dp_06_04_2021_line[1])
    a0_av = mainData.smartSchool.avg(a0_06_04_2021_line[1])

    return jsonify([[temp_06_04_2021_line.tolist(), humid_06_04_2021_line.tolist(), dp_06_04_2021_line.tolist(), a0_06_04_2021_line.tolist()],[temp_av, humid_av, dp_av, a0_av], myDate])

if __name__ == '__main__':
    #app.run(host="192.168.25.104")
    app.run(debug=True)
