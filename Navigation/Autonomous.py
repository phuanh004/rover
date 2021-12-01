#robot_simpleping.py
#uses an avoid function for obstacles

from gpiozero import Robot, DistanceSensor
from time import sleep
import random

#Define Motor Driver and encoder GPIO pins 
##################################################
# Motor A, Left Side GPIO CONSTANTS
PWML = 21        # PWMA - H-Bridge enable pin
FL = 20        # AI1 - Forward Drive
RL = 16          # AI2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWMR = 5       # PWMB - H-Bridge enable pin
FR = 13         # BI1 - Forward Drive
RR = 19         # BI2 - Reverse Drive
ECHO = 23        #echo pin on distance sensor
TRIG = 24       #trigger pin on distance sensor
RDISK = 17      # Encoder disk on the right rear wheel
# initialize distance sensor object for threshold of .3m
sensor = DistanceSensor(ECHO,TRIG, max_distance=1, threshold_distance=.3)
TDIST = 0.3

# robot object:pins are forward, reverse left, then right		
rover = Robot((FL,RL,PWML), (FR,RR,PWMR))	
#fwd/bk speed, spin turn speed and curve speeds
FSPD = 1
BSPD = .4
TSPD = BSPD * 1.75
CSPD = 1
 
#function for obstacle avoidance
def avoid():
    print (f"{(sensor.distance * 100):.1f}, cm, too close!")
    #print(sensor.distance * 100, " cm,  too close!")
    rover.stop()
    sleep(.5)
    rand = random.randint(0,9)
    if rand % 2 == 0:
        print (f"The number is even, back up to the right")
        rover.backward(TSPD,curve_right=CSPD)
    else:
        print (f"The number is odd, back up to the left")
        rover.backward(TSPD,curve_left=CSPD)
    sleep(.5)
    print ("ok, keep going")

def main():
    while True:
        if sensor.distance > TDIST:       
            rover.forward(FSPD)
        sensor.when_in_range = avoid    #when_in_range is builtin method
        sleep(.1)
main()