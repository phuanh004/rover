from gpiozero import Robot, DistanceSensor
from time import sleep
import random
import os
from dotenv import load_dotenv

load_dotenv()

# fwd/bk speed, spin turn speed and curve speeds
FSPD = 1
BSPD = .4
TSPD = BSPD * 1.75
CSPD = 1

# distance sensor
sensor = DistanceSensor(os.getenv('ECHO'), os.getenv('TRIG'), max_distance=1, threshold_distance=.3)

# robot object:pins are forward, reverse left, then right
rover = Robot(
	(os.getenv('MOTOR_A_FL'), os.getenv('MOTOR_A_RL'), os.getenv('MOTOR_A_PWML')),
	(os.getenv('MOTOR_B_FR'), os.getenv('MOTOR_B_RR'), os.getenv('MOTOR_B_PWMR'))
)

# function for obstacle avoidance


def avoid():
	print(f"{(sensor.distance * 100):.1f}, cm, too close!")
	#print(sensor.distance * 100, " cm,  too close!")
	rover.stop()
	sleep(.5)
	rand = random.randint(0, 9)
	if rand % 2 == 0:
		print(f"The number is even, back up to the right")
		rover.backward(TSPD, curve_right=CSPD)
	else:
		print(f"The number is odd, back up to the left")
		rover.backward(TSPD, curve_left=CSPD)
	sleep(.5)
	print("ok, keep going")


def main():
	while True:
		if sensor.distance > os.getenv('TDIST'):
			rover.forward(FSPD)
		sensor.when_in_range = avoid  # when_in_range is builtin method
		sleep(.1)


main()