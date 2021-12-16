import adafruit_dht
import asyncio
import board
import os
from dotenv import load_dotenv
from quart import Quart, websocket

from time import sleep
import json

# Load environment
load_dotenv()

SENSOR_TYPE = getattr(adafruit_dht, os.getenv("TEMP_SENSOR_TYPE"))
SENSOR_GPIO = getattr(board, os.getenv("TEMP_SENSOR_GPIO"))

# Initial the dht device, with data pin connected to:
dhtDevice = SENSOR_TYPE(SENSOR_GPIO)

# Quart App
app = Quart(__name__)

# Earth data
earth_data = {"temperature": 0, "humidity": 0, "radiation": 0}


@app.websocket("/temperature")
async def temperature():
    device_attribute = "temperature"
    while True:
        await websocket.send(
            json.dumps(
                {"error": "", "result": {"temperature_c": earth_data[device_attribute]}}
            )
        )
        earth_data[device_attribute] = get_dht_device_value(device_attribute)
        await asyncio.sleep(2)


@app.websocket("/humidity")
async def humidity():
    device_attribute = "humidity"
    while True:
        await websocket.send(
            json.dumps(
                {
                    "error": "",
                    "result": {device_attribute: earth_data[device_attribute]},
                }
            )
        )

        earth_data[device_attribute] = get_dht_device_value(device_attribute)
        await asyncio.sleep(2)


# TODO: Replace with radiation
@app.websocket("/radiation")
async def radiation():
    device_attribute = "radiation"
    while True:
        await websocket.send(
            json.dumps(
                {
                    "error": "",
                    "result": {device_attribute: earth_data[device_attribute]},
                }
            )
        )
        await asyncio.sleep(2)


def get_dht_device_value(device_attr):
    try:
        return getattr(dhtDevice, device_attr)

    except RuntimeError as error:
        print(error.args[0])

    except Exception as error:
        dhtDevice.exit()

    return earth_data[device_attr]


# Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
