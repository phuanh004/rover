import adafruit_dht
import board
import os
from dotenv import load_dotenv
from quart import Quart

# Load environment
load_dotenv()

SENSOR_TYPE = getattr(adafruit_dht, os.getenv('TEMP_SENSOR_TYPE'))
SENSOR_GPIO = getattr(board, os.getenv('TEMP_SENSOR_GPIO'))

# Initial the dht device, with data pin connected to:
dhtDevice = SENSOR_TYPE(SENSOR_GPIO)

# Quart App
app = Quart(__name__)


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

# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
