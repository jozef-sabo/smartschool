from flask import Flask, jsonify
import main

app = Flask(__name__)


@app.route('/')
def hello():
    return "Ahoj svet!\n"

@app.route('/sk')
def retrieve_all_data_from_all_sensors():
    db = main.fetchData.fetch()
    tempAll = main.smartSchool.filterByType(db, "Temperature")
    temp_05_04_2021 = main.smartSchool.filterByDateTime(tempAll, '2021', '04', '05', '0')
    print(type(temp_05_04_2021))
    print(jsonify(temp_05_04_2021.tolist()))
    return jsonify(temp_05_04_2021.tolist())

if __name__ == '__main__':
    # app.run(host="192.168.25.104")
    app.run(debug=True)