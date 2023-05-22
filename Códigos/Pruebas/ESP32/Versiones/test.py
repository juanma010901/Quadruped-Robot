import adafruit_pca9685
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import analogio
import board
import busio
import digitalio
import json
import math
import secrets
import socketpool
import ssl
import time
import wifi
from adafruit_motor import servo
import adafruit_requests as requests

#---------------------------------------------------------------------------------

ssid = secrets.secrets["ssid"]
password = secrets.secrets["password"]
aio_username = secrets.secrets["aio_username"]
aio_key = secrets.secrets["aio_key"]
#ssid = "Redmi"
#password = "987654321"

puntos = "https://masterusers.azurewebsites.net/api/GetPuntos"

wifi.radio.connect(ssid, password)
print("Connected to %s!" % ssid)
print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
https = requests.Session(pool, ssl.create_default_context())

#Puntos
def puntosP1():
    x = [json[0]["p1X"], json[1]["p1X"], json[2]["p1X"]]
    y = [json[0]["p1Y"], json[1]["p1Y"], json[2]["p1Y"]]
    return ([x, y])

def puntosP2():
    x = [json[0]["p2X"], json[1]["p2X"], json[2]["p2X"]]
    y = [json[0]["p2Y"], json[1]["p2Y"], json[2]["p2Y"]]
    return ([x, y])

def puntosP3():
    x = [json[0]["p3X"], json[1]["p3X"], json[2]["p3X"]]
    y = [json[0]["p3Y"], json[1]["p3Y"], json[2]["p3Y"]]
    return ([x, y])

def puntosP4():
    x = [json[0]["p4X"], json[1]["p4X"], json[2]["p4X"]]
    y = [json[0]["p4Y"], json[1]["p4Y"], json[2]["p4Y"]]
    return ([x, y])

def puntosHome():
    puntosIzquierda = [json[0]["p1X"], json[0]["p1Y"]]
    puntosDerecha = [json[0]["p3X"], json[0]["p3Y"]]
    return([puntosIzquierda, puntosDerecha])

def puntosHomeDefecto():
    puntosIzquierda = [0, 14]
    puntosDerecha = [2, 14]
    return([puntosIzquierda, puntosDerecha])

# Definición de pines I2C
SDA = board.D21
SCL = board.D22

# Configuración del bus I2C
i2c = busio.I2C(SCL, SDA)
pca = adafruit_pca9685.PCA9685(i2c, address=0x40)
pca.frequency = 50

# Configuración del Servomotor
servo_1 = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)
servo_2 = servo.Servo(pca.channels[2], min_pulse=500, max_pulse=2500)
servo_3 = servo.Servo(pca.channels[4], min_pulse=500, max_pulse=2500)
servo_4 = servo.Servo(pca.channels[6], min_pulse=500, max_pulse=2500)
servo_5 = servo.Servo(pca.channels[8], min_pulse=500, max_pulse=2500)
servo_6 = servo.Servo(pca.channels[10], min_pulse=500, max_pulse=2500)
servo_7 = servo.Servo(pca.channels[12], min_pulse=500, max_pulse=2500)
servo_8 = servo.Servo(pca.channels[14], min_pulse=500, max_pulse=2500)

# Definir las longitudes de las dos articulaciones del robot
l1 = 11
l2 = 13

# Funcion inversa izquierda
def inversaIzquierda(x, y):
    #print("Punto:" + str(x[i]) + "," + str(y[i]))
    #Calcular el valor de theta 2
    theta2 = math.acos((x**2 + y**2 - l1**2 - l2**2) / (2*l1*l2))

    # Calcular el valor de theta 1
    theta1 = math.atan2(y, x) + math.atan2(l2*math.sin(theta2), l1+l2*math.cos(theta2))
    
    #Angulos corregidos
    theta1c = math.degrees(theta1) - 90
    theta2c = 140 - math.degrees(theta2)

    return([theta1c,theta2c])

# Funcion inversa derecha
def inversaDerecha(x, y):
    #print("Punto:" + str(x[i]) + "," + str(y[i]))
    #Calcular el valor de theta 2
    theta2 = math.acos((x**2 + y**2 - l1**2 - l2**2) / (2*l1*l2))

    # Calcular el valor de theta 1
    theta1 = math.atan2(y, x) - math.atan2(l2*math.sin(theta2), l1+l2*math.cos(theta2))
    
    #Angulos corregidos
    theta1c = math.degrees(theta1)
    theta2c = math.degrees(theta2) + 40

    return([theta1c,theta2c])

# Mover Pata 1 (izquierda)
def calcularAngulosP1():
    
    # Invocar los puntos para mover las patas izquierdas
    puntos = puntosP1()
    x = puntos[0]
    y = puntos[1]

    angulosP1 = []

    for i in range(len(x)):
        angulosP1.append(inversaIzquierda(x[i],y[i]))
    return angulosP1

# Mover Pata 2 (izquierda)
def calcularAngulosP2():
    #Definir los vectores x e y
    puntos = puntosP2()
    x = puntos[0]
    y = puntos[1]

    angulosP2 = []

    for i in range(len(x)):
        angulosP2.append(inversaIzquierda(x[i],y[i]))
    return angulosP2
    
# Mover Pata 3 (derecha)
def calcularAngulosP3():
    #Definir los vectores x e y
    puntos = puntosP3()
    x = puntos[0]
    y = puntos[1]

    angulosP3 = []

    for i in range(len(x)):
        angulosP3.append(inversaDerecha(x[i],y[i]))
    return angulosP3

# Mover Pata 4 (derecha)
def calcularAngulosP4():
    puntos = puntosP4()
    x = puntos[0]
    y = puntos[1]

    angulosP4 = []

    for i in range(len(x)):
        angulosP4.append(inversaDerecha(x[i],y[i]))
    return angulosP4

#Funciones para mover las patas e imprimir la información
def moverP1(puntosP1):
    for i in range(len(puntosP1)):
            servo_1.angle = puntosP1[i][0]
            servo_2.angle = puntosP1[i][1]
            time.sleep(0.6)
            
def moverP2(puntosP2):
    for i in range(len(puntosP2)):
            servo_3.angle = puntosP2[i][0]
            servo_4.angle = puntosP2[i][1]
            time.sleep(0.6)
            
def moverP3(puntosP3):
    for i in range(len(puntosP3)):
            servo_5.angle = puntosP3[i][0]
            servo_6.angle = puntosP3[i][1]
            time.sleep(0.6)
            
def moverP4(puntosP4):
    for i in range(len(puntosP4)):
            servo_7.angle = puntosP4[i][0]
            servo_8.angle = puntosP4[i][1]
            time.sleep(0.6)

#---------------------------------------------------------------------------------
            
def moverP1P3(puntosP1, puntosP3):
    for i in range(len(puntosP1)):
            servo_1.angle = puntosP1[i][0]
            servo_2.angle = puntosP1[i][1]
            servo_5.angle = puntosP3[i][0]
            servo_6.angle = puntosP3[i][1]
            time.sleep(0.6)
            
def moverP2P4(puntosP2, puntosP4):
    for i in range(len(puntosP2)):
            servo_3.angle = puntosP2[i][0]
            servo_4.angle = puntosP2[i][1]
            servo_7.angle = puntosP4[i][0]
            servo_8.angle = puntosP4[i][1]
            time.sleep(0.6)
            
#---------------------------------------------------------------------------------


#Definición del Home (correr postura inicial por defecto)
def homeDefecto():
    home = puntosHomeDefecto()
    servo_1.angle, servo_2.angle = inversaIzquierda(home[0][0], home[0][1])
    servo_3.angle, servo_4.angle = inversaIzquierda(home[0][0], home[0][1])
    servo_5.angle, servo_6.angle = inversaDerecha(home[1][0], home[1][1])
    servo_7.angle, servo_8.angle = inversaDerecha(home[1][0], home[1][1])
    #time.sleep(0.1)
            
#---------------------------------------------------------------------------------        
            
def home():
    home = puntosHome()
    servo_1.angle, servo_2.angle = inversaIzquierda(home[0][0], home[0][1])
    servo_3.angle, servo_4.angle = inversaIzquierda(home[0][0], home[0][1])
    servo_5.angle, servo_6.angle = inversaDerecha(home[1][0], home[1][1])
    servo_7.angle, servo_8.angle = inversaDerecha(home[1][0], home[1][1])
    #time.sleep(0.1)
                        
            
#Marcha sencilla en la que se mueve un paso a la vez        
def marchaSencilla():
    moverP1(calcularAngulosP1())
    time.sleep(0.1)
    moverP3(calcularAngulosP3())
    time.sleep(0.1)
    moverP4(calcularAngulosP4())
    time.sleep(0.1)
    moverP2(calcularAngulosP2())
    time.sleep(0.1)

#---------------------------------------------------------------------------------

#Marcha de dos patas a la vez
def marchaDoble():
    moverP1P3(calcularAngulosP1(), calcularAngulosP3())
    time.sleep(0.1)
    moverP2P4(calcularAngulosP2(), calcularAngulosP4())
    time.sleep(0.1)
    
#---------------------------------------------------------------------------------

homeDefecto()

json = {}

while True:
    print("Fetching text from %s" % puntos)
    response = https.get(puntos)
    json = response.json()
    response.close()
    print(json)
    
    if len(json)==3:
        puntosP1()
        puntosP2()
        puntosP3()
        puntosP4()
        marchaSencilla()
    else:
        puntosHome()
        home()
    
    time.sleep(0.5)




















