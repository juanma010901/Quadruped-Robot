import time 
import board
import pwmio #Crear PMWs
from adafruit_motor import servo #Mover servomotores
import math #Operaciones matem'aticas(tangente inversa)
import board #Importar la placa de desarrollo
import analogio #Lectura de valores analogos

# Configurar el pin 26 como entrada analógica
pin_adc1 = analogio.AnalogIn(board.GP26)
pin_adc2 = analogio.AnalogIn(board.GP27)

# create a PWMOut object on Pin A2.
pwm1 = pwmio.PWMOut(board.GP2, duty_cycle=2 ** 15, frequency=50)
pwm2 = pwmio.PWMOut(board.GP3, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
my_servo1 = servo.Servo(pwm1, min_pulse=500, max_pulse=2500)
my_servo2 = servo.Servo(pwm2, min_pulse=500, max_pulse=2500)

#Definir los vectores x e y
x = [0, -4, -8, 0]
y = [14, 8, 14, 14]
#x = [4, -12, 1, -9, 14, 12, 16, 8, -4, -4, 18, -3, 5, -5, -10, 12, -7, 1, 2, 11]
#y = [19, 16, 16, 17, 1, 6, 1, 14, 15, 18, 10, 21, 19, 21, 14, 5, 12, 13, 18, 11]

# Definir las longitudes de las dos articulaciones del robot
l1 = 11
l2 = 12

#Declaracion de patas para definir marcha

while True:
    
    # Calcular theta1 y theta2 para cada valor de x e y
    for i in range(len(x)):
        print("Punto:" + str(x[i]) + "," + str(y[i]))
        #Calcular el valor de theta 2
        theta2 = math.acos((x[i]**2 + y[i]**2 - l1**2 - l2**2) / (2*l1*l2))

        # Calcular el valor de theta 1
        theta1 = math.atan2(y[i], x[i]) - math.atan2(l2*math.sin(theta2), l1+l2*math.cos(theta2))
        
        #Angulos corregidos
        theta1c = math.degrees(theta1)
        theta2c = math.degrees(theta2)
        
        #Enviar a angulo corregido
        my_servo1.angle = theta1c
        my_servo2.angle = theta2c + 40
        
        time.sleep(1)
        
        # Leer el valor del voltaje en el pin (en milivoltios)
        voltaje1 = pin_adc1.value * 3.3 / 65535.0
        voltaje2 = pin_adc2.value * 3.3 / 65535.0

        #Linezalización del voltaje para conocer los grados, según ecuación hallada
        grados1 = (((voltaje1-0.437999999)/0.0144166667))
        grados2 = 140-(((voltaje2-0.437999999)/0.0144166667))

        # Imprimir los valores de theta1 y theta2
        #print("Voltajes: ", voltaje1, voltaje2, "Valores Teóricos Corregidos: ", theta1c, theta2c, "Valores Experimentales: ", grados1, grados2)
        print("Grados M1:",  "Voltajes: ", voltaje1, voltaje2, "Valores Teóricos Corregidos: ", theta1c, theta2c, "Valores Experimentales: ", grados1-5, grados2-5)

        #print(str(voltaje1) + "," + str(voltaje2) + "," + str(theta1c) + "," + str(theta2c) + "," + str(grados1) + "," + str(grados2))
         
            
            
