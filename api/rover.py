import asyncio
from direction import Direction
from gpiozero import Robot
from motor import Motor
import os
from dotenv import load_dotenv

load_dotenv()


class Rover:
    def __init__(self) -> None:
        self.rv = Robot(
            (os.getenv('MOTOR_A_FL'), os.getenv(
                'MOTOR_A_RL'), os.getenv('MOTOR_A_PWML')),
            (os.getenv('MOTOR_B_FR'), os.getenv(
                'MOTOR_B_RR'), os.getenv('MOTOR_B_PWMR'))
        )

    def move(self, direction: Direction):
        if direction == direction.FORWARD:
            self.rv.forward(Motor.FWD_SPD)
        elif direction == direction.BACKWARD:
            self.rv.backward(Motor.RWD_SPD)
        elif direction == direction.FORWARD_LEFT:
            self.rv.forward(curve_left=Motor.CURVE_SPD)
        elif direction == direction.FORWARD_RIGHT:
            self.rv.forward(curve_right=Motor.CURVE_SPD)
        elif direction == direction.BACKWARD_LEFT:
            self.rv.backward(Motor.SPIN_TURN_SPD,
                             curve_left=Motor.CURVE_SPD)
        elif direction == direction.BACKWARD_RIGHT:
            self.rv.backward(Motor.SPIN_TURN_SPD,
                             curve_right=Motor.CURVE_SPD)
        else:
            self.stop()

    def stop(self):
        self.rv.stop()
