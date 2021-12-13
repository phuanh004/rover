import asyncio
from .direction import Direction
from gpiozero import Robot, DistanceSensor
from .motor import Motor
import os
from dotenv import load_dotenv
import random
from time import sleep

load_dotenv("../.env")


class Rover:
    def __init__(self) -> None:
        print(os.getenv('DISTANCE_SENSOR_ECHO'))
        print(os.getenv('DISTANCE_SENSOR_TRIG'))
        self.rv = Robot(
            (os.getenv('MOTOR_A_FL'), os.getenv(
                'MOTOR_A_RL'), os.getenv('MOTOR_A_PWML')),
            (os.getenv('MOTOR_B_FR'), os.getenv(
                'MOTOR_B_RR'), os.getenv('MOTOR_B_PWMR'))
        )
        self.vision = DistanceSensor(os.getenv('DISTANCE_SENSOR_ECHO'), os.getenv(
            'DISTANCE_SENSOR_TRIG'), max_distance=1, threshold_distance=.3)

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
        self.stop()
        rand_binary = random.random() < 0.5
        print("rand_binary")

        if rand_binary:
            self.move(Direction.BACKWARD_LEFT)
            print("backwardleft")
        else:
            self.move(Direction.BACKWARD_RIGHT)
            print("backwardright")
        sleep(.5)   


    def in_range(self):
        return self.vision.distance < Motor.DISTANCE_SENSOR_TRIGGER

    def stop(self):
        self.rv.stop()
