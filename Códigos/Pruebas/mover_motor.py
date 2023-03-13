# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Servo standard servo example"""
import time
import board
import pwmio
from adafruit_motor import servo

# create a PWMOut object on Pin A2.
pwm1 = pwmio.PWMOut(board.GP2, duty_cycle=2 ** 15, frequency=50)
pwm2 = pwmio.PWMOut(board.GP3, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo1 = servo.Servo(pwm1)
my_servo2 = servo.Servo(pwm2)


while True:
    angulo1 = float(input('Ingrese un angulo: '))
    angulo2 = float(input('Ingrese un angulo: '))
        
    
    # Patas del lado izquierdo tienen el 0 adelante por lo tanto se moveran hacia atrás
    my_servo1.angle = angulo1#+45
    my_servo2.angle = angulo2#-35

    
    # Patas del lado derecho tienen el 0 atrás por lo tanto se requiere el angulo suplementario para moverlas hacia atrás al igual que al lado izquierdo
    #my_servo1.angle = 180 - angulo
    #nmy_servo2.angle = 180 - angulo
    
    
    time.sleep(0.05)
                
    print("fin")
        
print("fin")
