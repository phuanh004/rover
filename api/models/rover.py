import asyncio
from .direction import Direction
from gpiozero import Robot, DistanceSensor
from .motor import Motor
import os
from dotenv import load_dotenv
import random
from time import sleep

load_dotenv("../.env")
load_dotenv()
sensor = DistanceSensor(os.getenv('ECHO'), os.getenv('TRIG'), max_distance=1, threshold_distance=.3)

class Rover:
    def __init__(self) -> None:
        print(os.getenv('ECHO'))
        print(os.getenv('TRIG'))
        self.rv = Robot(
            (os.getenv('MOTOR_A_FL'), os.getenv(
                'MOTOR_A_RL'), os.getenv('MOTOR_A_PWML')),
            (os.getenv('MOTOR_B_FR'), os.getenv(
                'MOTOR_B_RR'), os.getenv('MOTOR_B_PWMR'))
        )
        # self.vision = DistanceSensor(os.getenv('ECHO'), os.getenv('TRIG'), max_distance=1, threshold_distance=.3)

    def move(self, direction: Direction):
        if direction.FORWARD:
            self.rv.forward(Motor.FWD_SPD)
        elif direction.BACKWARD:
            self.rv.backward(Motor.RWD_SPD)
        elif direction.BACKWARD_LEFT:
            self.rv.backward(Motor.SPIN_TURN_SPD,
                             curve_left=Motor.CURVE_SPD)
        elif direction.BACKWARD_RIGHT:
            self.rv.backward(Motor.SPIN_TURN_SPD,
                             curve_right=Motor.CURVE_SPD)
        else:
            self.stop()

    def avoid_hazard(self):
        print(f"{(sensor.distance * 100):.1f}, cm, too close!")
	#print(sensor.distance * 100, " cm,  too close!")
        self.stop()
        sleep(.5)
        rand = random.randint(0, 9)
        if rand % 2 == 0:
            print(f"The number is even, back up to the right")
            self.rv.backward(Motor.SPIN_TURN_SPD, curve_right=Motor.CURVE_SPD)
        else:
            print(f"The number is odd, back up to the left")
            self.rv.backward(Motor.SPIN_TURN_SPD, curve_left=Motor.CURVE_SPD)
        sleep(.5)
        print("ok, keep going")


    def in_range(self):
        return sensor.distance < Motor.DISTANCE_SENSOR_TRIGGER

    def stop(self):
        self.rv.stop()
