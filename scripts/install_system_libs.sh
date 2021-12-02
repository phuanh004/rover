#!/bin/sh

# install libgpiod2 need for the temperature sensor
sudo apt-get update && apt-get install -y \
	libgpiod2 \
	&& rm -rf /var/lib/apt/lists/*