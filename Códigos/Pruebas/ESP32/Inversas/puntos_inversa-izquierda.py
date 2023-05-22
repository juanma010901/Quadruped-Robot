import time
import board
import pwmio
from adafruit_motor import servo
import math

# create a PWMOut object on Pin A2.
pwm1 = pwmio.PWMOut(board.D33, duty_cycle=2 ** 15, frequency=50)
pwm2 = pwmio.PWMOut(board.D32, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo1 = servo.Servo(pwm1, min_pulse=500, max_pulse=2500)
my_servo2 = servo.Servo(pwm2, min_pulse=500, max_pulse=2500)


while True:
    x = float(input('Ingrese punto en X: '))
    y = float(input('Ingrese punto en Y: '))
        
    # Definir las longitudes de las dos articulaciones del robot
    l1 = 11
    l2 = 13

    # Calcular el valor de theta 2
    theta2 = math.acos((x**2 + y**2 - l1**2 - l2**2) / (2*l1*l2))

    # Calcular el valor de theta 1
    theta1 = math.atan2(y, x) + math.atan2(l2*math.sin(theta2), l1+l2*math.cos(theta2)) 
    
    #Angulos corregidos
    theta1c = math.degrees(theta1)
    theta2c = 140 - math.degrees(theta2)
    
    #Enviar a angulo corregido
    my_servo1.angle = theta1c
    my_servo2.angle = theta2c
    
    # Imprimir los valores de theta 1 y theta 2 en grados y radianes
    print("Theta 1: ", math.degrees(theta1), "grados.", "Theta corregido 1: ", theta1c, "grados")
    print("Theta 2: ", math.degrees(theta2), "grados.", "Theta corregido 2: ", theta2c, "grados")  
    
    time.sleep(0.05)
                
        
print("fin")
