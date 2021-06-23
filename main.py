from flask import Flask, send_from_directory
from flask_session import Session
from app.aquarium import aquarium_api
from app.common import common
from app.smartschool import smartschool



# SESSION_COOKIE_SECURE = True
app = Flask(__name__, template_folder="app/static")
app.register_blueprint(aquarium_api)
app.register_blueprint(common)
app.register_blueprint(smartschool)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('app/static/css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('app/static/js', path)


if __name__ == '__main__':
    # app.run(host="192.168.25.104")
    # app.run(host="10.0.7.174", debug=True)
    # app.run(host="10.0.7.59", debug=True)
    app.run(host="localhost", debug=True)
