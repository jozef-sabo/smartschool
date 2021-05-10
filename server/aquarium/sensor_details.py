import requests
import flask


def cant_connect_to_aquarium(response: flask.Response):
    response.data = """{"error":"Cannot connect to aquarium"}"""
    response.status_code = 503
    return response


def get_all_sensors():
    r = requests.Response
    response = flask.Response()
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "http://192.168.1.111"
    try:
        r = requests.get("http://192.168.1.151/cm?cmnd=status%2010", timeout=0.5)
    except requests.exceptions.ConnectionError:
        return cant_connect_to_aquarium(response)
    else:
        response.data = r.text
        response.status_code = 200
        return response


def toggle_relay(to_state=None):
    r = requests.Response
    response = flask.Response()
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Origin"] = "http://192.168.1.111"
    try:
        if not to_state:
            r = requests.get("http://192.168.1.151/cm?cmnd=Power%20TOGGLE", timeout=0.5)
        else:
            request = "http://192.168.1.151/cm?cmnd=Power%20" + to_state if to_state in ("On","Off") else "http://192.168.1.151/cm?cmnd=Power"
            r = requests.get(request, timeout=0.5)
    except requests.exceptions.ConnectionError:
        return cant_connect_to_aquarium(response)
    else:
        response.data = r.text
        response.status_code = 200
        return response


if __name__ == '__main__':
    print(get_all_sensors().data)
