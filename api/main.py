import adafruit_dht
import asyncio
import board
import os
from dotenv import load_dotenv
from quart import Quart
from quart_cors import cors
from models.rover import Rover
from models.direction import Direction
from time import sleep

# Load environment
load_dotenv()

SENSOR_TYPE = getattr(adafruit_dht, os.getenv('TEMP_SENSOR_TYPE'))
SENSOR_GPIO = getattr(board, os.getenv('TEMP_SENSOR_GPIO'))

# Initial the dht device, with data pin connected to:
dhtDevice = SENSOR_TYPE(SENSOR_GPIO)

# Quart App
app = Quart(__name__)
app = cors(app, allow_origin="*")


@app.route('/temperature')
async def temperature():
    temp_c = dhtDevice.temperature
    temp_f = temp_c * (9 / 5) + 32

    return {
        "temp_c": temp_c,
        "temp_f": temp_f
    }


@app.route('/humidity')
async def humidity():
    humid = dhtDevice.humidity
    return {"humidity": humid}


# Rover
rover = Rover()
running = False


@app.route('/rover/start')
async def start_rover():
    global running
    global rover
    running = True

    while True:
        rover.move(direction=Direction.FORWARD)
        if rover.in_range():
            rover.avoid_hazard()
            sleep(.5)
        # return {"rover": "rover started"}


@app.route('/rover/stop')
async def stop_rover():
    global running
    global rover
    rover.stop()
    running = False

    return {"rover": "rover stopped"}


# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
