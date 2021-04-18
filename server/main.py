from flask import Flask, jsonify
import sensor_details
import mainData
import json


app = Flask(__name__)


@app.route('/')
def hello():
    return "Ahoj svet!\n"


@app.route('/get_sensors')
def retrieve_all_data_from_all_sensors():
    result = sensor_details.get_all_sensors()
    print(type(result))
    print(result)
    return jsonify(result)


@app.route('/Candle')
def filter_data_to_candle():
    db_data = mainData.fetchData.fetch()

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    # temp_today_candle = mainData.smartSchool.parseCandle(temp_today)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, '2021', '04', '06', '0')
    temp_06_04_2021_candle = mainData.smartSchool.parseCandle(temp_06_04_2021)

    humid_all = mainData.smartSchool.filterByType(db_data, "Humidity")
    # humid_today = mainData.smartSchool.filterTodayData(humid_all)
    # humid_today_candle = mainData.smartSchool.parseCandle(humid_today)
    humid_06_04_2021 = mainData.smartSchool.filterByDateTime(humid_all, '2021', '04', '06', '0')
    humid_06_04_2021_candle = mainData.smartSchool.parseCandle(humid_06_04_2021)

    dp_all = mainData.smartSchool.filterByType(db_data, "DewPoint")
    # dp_today = mainData.smartSchool.filterTodayData(dp_all)
    # dp_today_candle = mainData.smartSchool.parseCandle(dp_today)
    dp_06_04_2021 = mainData.smartSchool.filterByDateTime(dp_all, '2021', '04', '06', '0')
    dp_06_04_2021_candle = mainData.smartSchool.parseCandle(dp_06_04_2021)

    a0_all = mainData.smartSchool.filterByType(db_data, "A0")
    # a0_today = mainData.smartSchool.filterTodayData(a0_all)
    # a0_today_candle = mainData.smartSchool.parseCandle(a0_today)
    a0_06_04_2021 = mainData.smartSchool.filterByDateTime(a0_all, '2021', '04', '06', '0')
    a0_06_04_2021_candle = mainData.smartSchool.parseCandle(a0_06_04_2021)

    return jsonify([temp_06_04_2021_candle, humid_06_04_2021_candle, dp_06_04_2021_candle, a0_06_04_2021_candle])

@app.route('/Line')
def filter_data_to_line():
    db_data = mainData.fetchData.fetch()

    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    # temp_today = mainData.smartSchool.filterTodayData(temp_all)
    temp_06_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, '2021', '04', '06', '0')
    temp_06_04_2021_line = mainData.smartSchool.parsePlot(temp_06_04_2021)

    humid_all = mainData.smartSchool.filterByType(db_data, "Humidity")
    # humid_today = mainData.smartSchool.filterTodayData(humid_all)
    humid_06_04_2021 = mainData.smartSchool.filterByDateTime(humid_all, '2021', '04', '06', '0')
    humid_06_04_2021_line = mainData.smartSchool.parsePlot(humid_06_04_2021)

    dp_all = mainData.smartSchool.filterByType(db_data, "DewPoint")
    # dp_today = mainData.smartSchool.filterTodayData(dp_all)
    dp_06_04_2021 = mainData.smartSchool.filterByDateTime(dp_all, '2021', '04', '06', '0')
    dp_06_04_2021_line = mainData.smartSchool.parsePlot(dp_06_04_2021)

    a0_all = mainData.smartSchool.filterByType(db_data, "A0")
    # a0_today = mainData.smartSchool.filterTodayData(a0_all)
    a0_06_04_2021 = mainData.smartSchool.filterByDateTime(a0_all, '2021', '04', '06', '0')
    a0_06_04_2021_line = mainData.smartSchool.parsePlot(a0_06_04_2021)

    temp_av = mainData.smartSchool.avg(temp_06_04_2021_line[1])
    humid_av = mainData.smartSchool.avg(humid_06_04_2021_line[1])
    dp_av = mainData.smartSchool.avg(dp_06_04_2021_line[1])
    a0_av = mainData.smartSchool.avg(a0_06_04_2021_line[1])

    return jsonify([[temp_06_04_2021_line.tolist(), humid_06_04_2021_line.tolist(), dp_06_04_2021_line.tolist(), a0_06_04_2021_line.tolist()],[temp_av, humid_av, dp_av, a0_av]])

if __name__ == '__main__':
    #app.run(host="192.168.25.104")
    app.run(debug=True)
