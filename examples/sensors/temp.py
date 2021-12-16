import adafruit_dht
from board import D4
from time import sleep

dht_device = adafruit_dht.DHT11(D4)

temperature = dht_device.temperature
humidity = dht_device.humidity

while True:
    print(temperature)
    sleep(.5)
