import asyncio
from direction import Direction
from gpiozero import Robot, DistanceSensor
from motor import Motor
import os
from dotenv import load_dotenv
import random

load_dotenv()


class Rover:
    def __init__(self) -> None:
        self.rover = Robot(
            (os.getenv('MOTOR_A_FL'), os.getenv(
                'MOTOR_A_RL'), os.getenv('MOTOR_A_PWML')),
            (os.getenv('MOTO_A_FR'), os.getenv(
                'MOTO_A_RR'), os.getenv('MOTO_A_PWMR'))
        )
        self.vision = DistanceSensor(os.getenv('ECHO'), os.getenv(
            'TRIG'), max_distance=1, threshold_distance=.3)

    async def move(self, direction: Direction):
        if direction.FORWARD:
            self.rover.forward(Motor.FWD_SPD)
        elif direction.BACKWARD:
            self.rover.backward(Motor.RWD_SPD)
        elif direction.BACKWARD_LEFT:
            self.rover.backward(Motor.SPIN_TURN_SPD,
                                curve_left=Motor.CURVE_SPD)
        elif direction.BACKWARD_RIGHT:
            self.rover.backward(Motor.SPIN_TURN_SPD,
                                curve_right=Motor.CURVE_SPD)
        else:
            await self.stop()

    async def avoid_hazard(self):
        await self.stop()
        await asyncio.sleep(.5)
        rand_binary = random.random() < 0.5

        if rand_binary:
            await self.move(Direction.BACKWARD_LEFT)
        else:
            await self.move(Direction.BACKWARD_RIGHT)

        await asyncio.sleep(.5)

    def in_range(self):
        return self.vision.distance < Motor.DISTANCE_SENSOR_TRIGGER

    async def stop(self):
        self.rover.stop()
