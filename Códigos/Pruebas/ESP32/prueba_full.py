import time
import board
import busio
import adafruit_pca9685
from adafruit_motor import servo
import digitalio
import analogio
import math

# Definición de pines I2C
SDA = board.D21
SCL = board.D22

# Definición de pin en alto (Alimentación de PCA)
#pin2 = digitalio.DigitalInOut(board.D2)
#pin2.direction = digitalio.Direction.OUTPUT
#pin2.value = True

# Configuración del bus I2C
i2c = busio.I2C(SCL, SDA)
pca = adafruit_pca9685.PCA9685(i2c, address=0x40)
pca.frequency = 50

# Configuración del Servomotor
servo_1 = servo.Servo(pca.channels[8], min_pulse=500, max_pulse=2500)
servo_2 = servo.Servo(pca.channels[10], min_pulse=500, max_pulse=2500)

# Configurar el pin 0,4 como entrada analógica
#pin_adc1 = analogio.AnalogIn(board.D)
#pin_adc2 = analogio.AnalogIn(board.D15)

#Definir los vectores x e y
x = [0, 4, 8, 0]
y = [14, 8, 14, 14]

# Definir las longitudes de las dos articulaciones del robot
l1 = 11
l2 = 13

while True:
    
    # Mover el Servomotor a 0 grados
    #angle = int(input("Ingrese Ángulo: "))
    #servo_1.angle = angle
    
    for i in range(len(x)):
        print("Punto:" + str(x[i]) + "," + str(y[i]))
        #Calcular el valor de theta 2
        theta2 = math.acos((x[i]**2 + y[i]**2 - l1**2 - l2**2) / (2*l1*l2))

        # Calcular el valor de theta 1
        theta1 = math.atan2(y[i], x[i]) + math.atan2(l2*math.sin(theta2), l1+l2*math.cos(theta2))
        
        #Angulos corregidos
        theta1c = math.degrees(theta1)
        theta2c = 140 - math.degrees(theta2)
        
        #Enviar a angulo corregido
        servo_1.angle = theta1c
        servo_2.angle = theta2c
        
        time.sleep(1)
        
        # Leer el valor del voltaje en el pin (en milivoltios)
        #voltaje1 = pin_adc1.value * 3.3 / 65535.0
        #voltaje2 = pin_adc2.value * 3.3 / 65535.0

        #Linezalización del voltaje para conocer los grados, según ecuación hallada
        #grados1 = (((voltaje1-0.437999999)/0.0144166667))
        #grados2 = 140-(((voltaje2-0.437999999)/0.0144166667))

        # Imprimir los valores de theta1 y theta2
        #print("Voltajes: ", voltaje1, voltaje2, "Valores Teóricos Corregidos: ", theta1c, theta2c, "Valores Experimentales: ", grados1, grados2)
        #print("Voltajes: ", voltaje1, voltaje2, "Valores Teóricos Corregidos: ", theta1c, theta2c, "Valores Experimentales: ", grados1-5, grados2-5)
        print("Valores Teóricos Corregidos: ", theta1c, theta2c, "Valores Experimentales: ")
    
    
    