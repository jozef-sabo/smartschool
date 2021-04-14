from flask import Flask, jsonify
import sensor_details
import mainData


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


@app.route('/timelineTemp')
def filter_data_to_plot():
    db_data = mainData.fetchData.fetch()
    temp_all = mainData.smartSchool.filterByType(db_data, "Temperature")
    temp_05_04_2021 = mainData.smartSchool.filterByDateTime(temp_all, '2021', '04', '06', '0')
    # print(type(temp_05_04_2021))
    # print(jsonify(temp_05_04_2021.tolist()))
    return jsonify(temp_05_04_2021.tolist())


if __name__ == '__main__':
    #app.run(host="192.168.25.104")
    app.run(debug=True)
