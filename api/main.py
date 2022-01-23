import adafruit_dht
import asyncio
import board
import os
from dotenv import load_dotenv
import json
from gpiozero import DistanceSensor

from direction import Direction
from quart import Quart, websocket
from rover import Rover

import exixe
import spidev
import time
import datetime
import RPi.GPIO as GPIO
from collections import deque

# Load environment
load_dotenv()

SENSOR_TYPE = getattr(adafruit_dht, os.getenv("TEMP_SENSOR_TYPE"))
SENSOR_GPIO = getattr(board, os.getenv("TEMP_SENSOR_GPIO"))

rv = Rover()

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
                {"error": "", "result": {
                    "temperature_c": earth_data[device_attribute]}}
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
counts = deque()
hundredcount = 0


def countme(channel):
    global counts, hundredcount
    timestamp = datetime.datetime.now()
    counts.append(timestamp)

    # Every time we hit 100 counts, run count100 and reset
    hundredcount = hundredcount + 1
    if hundredcount >= 100:
        hundredcount = 0
        count100()

# This method runs the servo to increment the mechanical counter


def count100():
    GPIO.setup(12, GPIO.OUT)
    pwm = GPIO.PWM(12, 50)

    pwm.start(4)
    time.sleep(1)
    pwm.start(9.5)
    time.sleep(1)
    pwm.stop()


# Set the input with falling edge detection for geiger counter pulses
GPIO.setup(4, GPIO.IN)
GPIO.add_event_detect(4, GPIO.FALLING, callback=countme)

# Initialize everything needed for the Exixe Nixie tube drivers
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 7800000

cs_pin = 15
cs_pin_m = 13
cs_pin_r = 11

my_tube = exixe.Exixe(cs_pin, spi)
my_tube_m = exixe.Exixe(cs_pin_m, spi, overdrive=True)
my_tube_r = exixe.Exixe(cs_pin_r, spi)

my_tube.set_led(127, 28, 0)
my_tube_m.set_led(127, 28, 0)
my_tube_r.set_led(127, 28, 0)

loop_count = 0


@app.websocket("/radiation")
async def radiation():
    device_attribute = "radiation"

    global loop_count

    while True:
        loop_count = loop_count + 1

        try:
            while counts[0] < datetime.datetime.now() - datetime.timedelta(seconds=60):
                counts.popleft()
        except IndexError:
            pass  # there are no records in the queue.

        if loop_count == 10:
            earth_data[device_attribute] = int(len(counts))
            loop_count = 0

        # Update the displays with a zero-padded string
        text_count = f"{len(counts):0>3}"
        my_tube.set_digit(int(text_count[0]))
        my_tube_m.set_digit(int(text_count[1]))
        my_tube_r.set_digit(int(text_count[2]))

        await websocket.send(
            json.dumps(
                {
                    "error": "",
                    "result": {device_attribute: earth_data[device_attribute]},
                }
            )
        )

        await asyncio.sleep(1)


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
async def rover_move_fwd():
    while True:
        cmd = await websocket.receive()
        if cmd == "left":
            rv.move(Direction.FORWARD_LEFT)
        elif cmd == "right":
            rv.move(Direction.FORWARD_RIGHT)
        else:
            rv.move(Direction.FORWARD)


@app.websocket("/rover/move/backward")
async def rover_move_bwd():
    while True:
        cmd = await websocket.receive()
        if cmd == "left":
            rv.move(Direction.BACKWARD_LEFT)
        elif cmd == "right":
            rv.move(Direction.BACKWARD_RIGHT)
        elif cmd == "stop":
            rv.stop()
        else:
            rv.move(Direction.BACKWARD)


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
