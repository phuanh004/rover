import asyncio
from gpiozero import Robot
import os
from dotenv import load_dotenv
from enum import Enum
import random

load_dotenv()


class Motor:
    FWD_SPD = 1
    BKWD_SPD = .4
    SPIN_TURN_SPD = BKWD_SPD * 1.75
    CURVE_SPD = 1
    DISTANCE_SENSOR_TRIGGER = 0.3


class Direction(Enum):
    FORWARD = "fwd"
    BACKWARD = "bwd"
    BACKWARD_LEFT = "bwd_l"
    BACKWARD_RIGHT = "bwd_r"


class Rover:
    def __init__(self) -> None:
        self.rover = Robot(
            (os.getenv('MOTOR_A_FL'), os.getenv(
                'MOTOR_A_RL'), os.getenv('MOTOR_A_PWML')),
            (os.getenv('MOTO_A_FR'), os.getenv(
                'MOTO_A_RR'), os.getenv('MOTO_A_PWMR'))
        )

    async def move(self, direction: Direction):
        if(direction.FORWARD):
            self.rover.forward(Motor.FWD_SPD)
        elif(direction.BACKWARD):
            self.rover.backward(Motor.BKWD_SPD)
        elif(direction.BACKWARD_LEFT):
            self.rover.backward(Motor.SPIN_TURN_SPD,
                                curve_left=Motor.CURVE_SPD)
        elif(direction.BACKWARD_RIGHT):
            self.rover.backward(Motor.SPIN_TURN_SPD,
                                curve_right=Motor.CURVE_SPD)
        else:
            self.stop

    async def avoid_hazzard(self):
        self.stop
        await asyncio.sleep(.5)
        rand_binary = random.random() < 0.5

        if(rand_binary):
            self.move(Direction.BACKWARD_LEFT)
        else:
            self.move(Direction.BACKWARD_RIGHT)

        self.sensor.when_in_range = self.stop  # when_in_range is builtin method
        await asyncio.sleep(.1)

    async def stop(self):
        self.rover.stop
