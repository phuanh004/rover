import adafruit_dht
import asyncio
import board
import os
from dotenv import load_dotenv
from quart import Quart, websocket
from gpiozero import DistanceSensor, Robot

from time import sleep
import json

# Load environment
load_dotenv()

SENSOR_TYPE = getattr(adafruit_dht, os.getenv("TEMP_SENSOR_TYPE"))
SENSOR_GPIO = getattr(board, os.getenv("TEMP_SENSOR_GPIO"))

rv = Robot(
    (os.getenv("MOTOR_A_FL"), os.getenv("MOTOR_A_RL"), os.getenv("MOTOR_A_PWML")),
    (os.getenv("MOTOR_B_FR"), os.getenv("MOTOR_B_RR"), os.getenv("MOTOR_B_PWMR")),
)

# distance sensor
sensor = DistanceSensor(
    os.getenv("DISTANCE_SENSOR_ECHO"),
    os.getenv("DISTANCE_SENSOR_TRIG"),
    max_distance=1,
    threshold_distance=0.3,
)

# Initial the dht device, with data pin connected to:
dhtDevice = SENSOR_TYPE(SENSOR_GPIO)

# Quart App
app = Quart(__name__)

# Earth data
earth_data = {"temperature": 0, "humidity": 0, "radiation": 0}
rover_data = {"distance": 100}


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


@app.websocket("/distance")
async def distance():
    device_attribute = "distance"
    while True:
        await websocket.send(
            json.dumps(
                {
                    "error": "",
                    "result": {device_attribute: rover_data[device_attribute]},
                }
            )
        )
        rover_data[device_attribute] = sensor.distance * 100
        await asyncio.sleep(0.2)


@app.websocket("/rover/move/forward")
async def rove_move():
    while True:
        cmd = await websocket.receive()
        if cmd == "left":
            rv.forward(0.4 * 1.75, curve_left=1)
        else:
            rv.forward(1)


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
