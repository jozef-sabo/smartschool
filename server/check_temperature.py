import json
import sensor_details

response = sensor_details.get_sensors_aquarium()
response_text = json.loads(response.data)

if "error" not in response_text:
    if int(response_text["w_temp"]) < 25 or int(response_text["a_temp"]) < 35:
        sensor_details.toggle_relay("1", "On")

    if int(response_text["w_temp"]) > 28 or int(response_text["a_temp"]) > 40:
        sensor_details.toggle_relay("1", "Off")
