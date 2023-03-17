from adafruit_motor import servo
import adafruit_pca9685
import analogio
import board
import busio
import digitalio
import math
import time

# Definición de pines I2C
SDA = board.D21
SCL = board.D22

# Configuración del bus I2C
i2c = busio.I2C(SCL, SDA)
pca = adafruit_pca9685.PCA9685(i2c, address=0x40)
pca.frequency = 50

# Create a servo object, my_servo.
servo1 = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)
servo2 = servo.Servo(pca.channels[2], min_pulse=500, max_pulse=2500)
servo3 = servo.Servo(pca.channels[4], min_pulse=500, max_pulse=2500)
servo4 = servo.Servo(pca.channels[6], min_pulse=500, max_pulse=2500)
servo5 = servo.Servo(pca.channels[8], min_pulse=500, max_pulse=2500)
servo6 = servo.Servo(pca.channels[10], min_pulse=500, max_pulse=2500)
servo7 = servo.Servo(pca.channels[12], min_pulse=500, max_pulse=2500)
servo8 = servo.Servo(pca.channels[14], min_pulse=500, max_pulse=2500)


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
    servo1.angle = theta1c
    servo2.angle = theta2c
    servo3.angle = theta1c
    servo4.angle = theta2c
    
    # Imprimir los valores de theta 1 y theta 2 en grados y radianes
    print("Theta 1: ", math.degrees(theta1), "grados.", "Theta corregido 1: ", theta1c, "grados")
    print("Theta 2: ", math.degrees(theta2), "grados.", "Theta corregido 2: ", theta2c, "grados")  
    
    time.sleep(0.05)
                
        
print("fin")
