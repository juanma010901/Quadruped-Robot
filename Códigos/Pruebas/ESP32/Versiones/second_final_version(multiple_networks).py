import adafruit_hcsr04
import adafruit_pca9685
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import adafruit_requests as requests
import analogio
import board
import busio
import digitalio
import ipaddress
import json
import math
import pulseio
import wifi_networks
import socketpool
import ssl
import time
import wifi
from adafruit_motor import servo

#---------------------------------------------------------------------------------

#EndPoints API
getPuntos = "https://masterusers.azurewebsites.net/api/GetPuntos"
getModo = "https://masterusers.azurewebsites.net/api/GetModoActual"
updateModo = "https://masterusers.azurewebsites.net/api/ActualizarModo"

wifi_networks.connect_to_network()

pool = socketpool.SocketPool(wifi.radio)
https = requests.Session(pool, ssl.create_default_context())

#---------------------------------------------------------------------------------

# Configura los LEDs
ledHome = digitalio.DigitalInOut(board.D5)
ledHome.direction = digitalio.Direction.OUTPUT
ledMarchas = digitalio.DigitalInOut(board.D18)
ledMarchas.direction = digitalio.Direction.OUTPUT
ledManiobras = digitalio.DigitalInOut(board.D19)
ledManiobras.direction = digitalio.Direction.OUTPUT
ledManual = digitalio.DigitalInOut(board.D23)
ledManual.direction = digitalio.Direction.OUTPUT

#--------------------------------------------------------------------------------
#Configuración de los ultrasonidos

# Configurar los pines Trig y Echo del sensor de ultrasonido
echo_pin1 = board.D34
echo_pin2 = board.D35
trig_pin1 = board.D32
trig_pin2 = board.D33

# Configurar el temporizador para medir la duración del pulso de eco
timer1 = pulseio.PulseIn(echo_pin1, maxlen=1)
timer2 = pulseio.PulseIn(echo_pin2, maxlen=1)

# Configurar el objeto del sensor de ultrasonido
sonar1 = adafruit_hcsr04.HCSR04(trigger_pin=trig_pin1, echo_pin=echo_pin1, timeout=0.1)
sonar2 = adafruit_hcsr04.HCSR04(trigger_pin=trig_pin2, echo_pin=echo_pin2, timeout=0.1)

#---------------------------------------------------------------------------------

#Suma
def puntosP1():
    x = [6, 9, 3]
    y = [11, 12, 13]
    return ([x, y])

def puntosP2():
    x = [0, 3, -3]
    y = [12, 14, 14]
    return ([x, y])

#Resta
def puntosP3():
    x = [0, -3, 3]
    y = [12, 14, 14]
    return ([x, y])

def puntosP4():
    x = [-3, -6, 0]
    y = [11, 12, 13]
    return ([x, y])

def puntosHome():
    puntosP1 = [3, 13]
    puntosP2 = [-3, 14]
    puntosP3 = [3, 14]
    puntosP4 = [0, 13]
    return([puntosP1, puntosP2, puntosP3, puntosP4])

def puntosAgachado():
    puntosP1 = [2, 9]
    puntosP2 = [-1, 9]
    puntosP3 = [1, 9]
    puntosP4 = [-1, 9]
    return([puntosP1, puntosP2, puntosP3, puntosP4])
    
def puntosParado():
    puntosP1 = [4, 20]
    puntosP2 = [-5, 21]
    puntosP3 = [5, 21]
    puntosP4 = [0, 20]
    return([puntosP1, puntosP2, puntosP3, puntosP4])

def puntosAdelante():
    puntosP1 = [6, 10]
    puntosP2 = [-1, 19]
    puntosP3 = [1, 19]
    puntosP4 = [-4, 10]
    return([puntosP1, puntosP2, puntosP3, puntosP4])

def puntosAtras():
    puntosP1 = [2, 17]
    puntosP2 = [-4, 11]
    puntosP3 = [4, 11]
    puntosP4 = [1, 17]
    return([puntosP1, puntosP2, puntosP3, puntosP4])

def puntosIzquierda():
    puntosP1 = [3, 11]
    puntosP2 = [-4, 11]
    puntosP3 = [4, 19]
    puntosP4 = [1, 19]
    return([puntosP1, puntosP2, puntosP3, puntosP4])

def puntosDerecha():
    puntosP1 = [3, 20]
    puntosP2 = [-3, 20]
    puntosP3 = [4, 12]
    puntosP4 = [-1, 12]
    return([puntosP1, puntosP2, puntosP3, puntosP4])

#---------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------

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
        time.sleep(0.3)
            
def moverP2P4(puntosP2, puntosP4):
    for i in range(len(puntosP2)):
            servo_3.angle = puntosP2[i][0]
            servo_4.angle = puntosP2[i][1]
            servo_7.angle = puntosP4[i][0]
            servo_8.angle = puntosP4[i][1]
            time.sleep(0.3)
      
#--------------------------------------------------------------------------------- 
            
def pararse():
    home = puntosHome()
    servo_3.angle, servo_4.angle = inversaIzquierda(home[1][0], home[1][1])
    servo_5.angle, servo_6.angle = inversaDerecha(home[2][0], home[2][1])
    time.sleep(0.3)
    servo_1.angle, servo_2.angle = inversaIzquierda(home[0][0], home[0][1])
    servo_7.angle, servo_8.angle = inversaDerecha(home[3][0], home[3][1])
    #time.sleep(0.1)
      
#--------------------------------------------------------------------------------- 
            
def home():
    home = puntosHome()
    servo_3.angle, servo_4.angle = inversaIzquierda(home[1][0], home[1][1])
    servo_5.angle, servo_6.angle = inversaDerecha(home[2][0], home[2][1])
    servo_1.angle, servo_2.angle = inversaIzquierda(home[0][0], home[0][1])
    servo_7.angle, servo_8.angle = inversaDerecha(home[3][0], home[3][1])
    #time.sleep(0.1)


#---------------------------------------------------------------------------------
            
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
            
def maniobraAgachado():
    agachado = puntosAgachado()
    servo_1.angle, servo_2.angle = inversaIzquierda(agachado[0][0], agachado[0][1])
    servo_3.angle, servo_4.angle = inversaIzquierda(agachado[1][0], agachado[1][1])
    servo_5.angle, servo_6.angle = inversaDerecha(agachado[2][0], agachado[2][1])
    servo_7.angle, servo_8.angle = inversaDerecha(agachado[3][0], agachado[3][1])
    #time.sleep(0.1)
    
#--------------------------------------------------------------------------------- 
    
def maniobraParado():
#     if(estadoAnterior == "Home"):
#         espera = 0.2
#     elif(estadoAnterior == "Maniobra agachado"):
#         espera = 0.35
# #     elif(estadoAnterior == "Agachado hacia atras"):
# #         servo_1.angle, servo_2.angle = inversaIzquierda(home[0][0], home[0][1])
# #         servo_7.angle, servo_8.angle = inversaDerecha(home[3][0], home[3][1])
#     else:
#         espera = 0.2
#         
    parado = puntosParado()
    servo_3.angle, servo_4.angle = inversaIzquierda(parado[1][0], parado[1][1])
    servo_5.angle, servo_6.angle = inversaDerecha(parado[2][0], parado[2][1])
    time.sleep(0.35)
    servo_1.angle, servo_2.angle = inversaIzquierda(parado[0][0], parado[0][1])
    servo_7.angle, servo_8.angle = inversaDerecha(parado[3][0], parado[3][1])
    #time.sleep(0.1)
    
#---------------------------------------------------------------------------------   

def maniobraInclinadoIzquierda():
    izquierda = puntosIzquierda()
    servo_1.angle, servo_2.angle = inversaIzquierda(izquierda[0][0], izquierda[0][1])
    servo_3.angle, servo_4.angle = inversaIzquierda(izquierda[1][0], izquierda[1][1])
    servo_5.angle, servo_6.angle = inversaDerecha(izquierda[2][0], izquierda[2][1])
    servo_7.angle, servo_8.angle = inversaDerecha(izquierda[3][0], izquierda[3][1])
    #time.sleep(0.1)
    
#---------------------------------------------------------------------------------   

def maniobraInclinadoDerecha():
    derecha = puntosDerecha()
    servo_1.angle, servo_2.angle = inversaIzquierda(derecha[0][0], derecha[0][1])
    servo_3.angle, servo_4.angle = inversaIzquierda(derecha[1][0], derecha[1][1])
    servo_5.angle, servo_6.angle = inversaDerecha(derecha[2][0], derecha[2][1])
    servo_7.angle, servo_8.angle = inversaDerecha(derecha[3][0], derecha[3][1])
    #time.sleep(0.1)

#--------------------------------------------------------------------------------- 
    
def maniobraInclinadoAdelante():
    adelante = puntosAdelante()
    servo_1.angle, servo_2.angle = inversaIzquierda(adelante[0][0], adelante[0][1])
    servo_3.angle, servo_4.angle = inversaIzquierda(adelante[1][0], adelante[1][1])
    servo_5.angle, servo_6.angle = inversaDerecha(adelante[2][0], adelante[2][1])
    servo_7.angle, servo_8.angle = inversaDerecha(adelante[3][0], adelante[3][1])
    #time.sleep(0.1)
    
#--------------------------------------------------------------------------------- 
    
def maniobraInclinadoAtras():
    atras = puntosAtras()
    servo_1.angle, servo_2.angle = inversaIzquierda(atras[0][0], atras[0][1])
    servo_3.angle, servo_4.angle = inversaIzquierda(atras[1][0], atras[1][1])
    servo_5.angle, servo_6.angle = inversaDerecha(atras[2][0], atras[2][1])
    servo_7.angle, servo_8.angle = inversaDerecha(atras[3][0], atras[3][1])
    #time.sleep(0.1)
    
#--------------------------------------------------------------------------------- 
   
def puntosManual():
    #print("Fetching text from %s" % getPuntos)
    response = https.get(getPuntos)
    puntos = response.json()
    response.close()
    print(puntos)
    print(type(puntos))
    
    #Pedir puntos de home para comparar en caso de que el enviado sea el Home
    home = puntosHome()
    x3h = home[2][0]
    x4h = home[3][0]
    print(x3h, x4h)
    
    x1 = puntos[0]["p1X"]
    y1 = puntos[0]["p1Y"]
    x2 = puntos[0]["p2X"]
    y2 = puntos[0]["p2Y"]
    x3 = puntos[0]["p3X"]
    y3 = puntos[0]["p3Y"]
    x4 = puntos[0]["p4X"]
    y4 = puntos[0]["p4Y"]
    try:
        servo_1.angle, servo_2.angle = inversaIzquierda(x1, y1)
        servo_3.angle, servo_4.angle = inversaIzquierda(x2, y2)
        if x3h == x3:
            servo_5.angle, servo_6.angle = inversaDerecha(x3, y3)
        else:
            servo_5.angle, servo_6.angle = inversaDerecha(-x3, y3)
        if x4h == x4:
            servo_7.angle, servo_8.angle = inversaDerecha(x4, y4)
        else:
            servo_7.angle, servo_8.angle = inversaDerecha(-x4, y4)
    except:
        print("Punto fuera de rango")
    
#---------------------------------------------------------------------------------  
    
# Definir la función de medición de distancia
def medir_distancia(sensor):
    try:
        if sensor == 1:
            distance1 = sonar1.distance
            return distance1
        elif sensor == 2:
            distance2 = sonar2.distance
            return distance2
    except:
        if sensor == 1:
            distance1 = 450
            return distance1
        elif sensor == 2:
            distance2 = 450
            return distance2

#--------------------------------------------------------------------------------- 
    
#Actualizar modo
def cambioHome():
    data = '{"Id":1,"Activo": true,"Descripcion": "Home","SeccionId": 1}\n'
    print("POSTing data to {0}: {1}".format(updateModo, data))
    response = https.put(updateModo, data=data)
    
#---------------------------------------------------------------------------------
    
    
#---------------------------------------------------------------------------------
#CICLO INFINITO
#--------------------------------------------------------------------------------- 
    
pararse()

json = {}

#estadoAnterior = ""
while True:
    
    print("Fetching text from %s" % getModo)
    response = https.get(getModo)
    info = response.json()
    response.close()
    print(info)
    #print(type(json))
    
    #estadoAnterior = estado
    estado = info["descripcion"]
    #print(estadoAnterior)
    #print(estado)
    
    if (estado == "Home"):
        ledHome.value = True
        home()
        time.sleep(1)
        ledHome.value = False
    elif (estado == "Maniobra agachado"):
        ledManiobras.value = True
        maniobraAgachado()
        time.sleep(1)
        ledManiobras.value = False
    elif (estado == "Maniobra parado"):
        ledManiobras.value = True
        maniobraParado()
        time.sleep(1)
        ledManiobras.value = False
    elif (estado == "Maniobra inclinado hacia adelante"):
        ledManiobras.value = True
        maniobraInclinadoAdelante()
        time.sleep(1)
        ledManiobras.value = False
    elif (estado == "Maniobra inclinado hacia atras"):
        ledManiobras.value = True
        maniobraInclinadoAtras()
        time.sleep(1)
        ledManiobras.value = False
    elif (estado == "Equilibrio dos patas izquierda"):
        ledManiobras.value = True
        maniobraInclinadoIzquierda()
        time.sleep(1)
        ledManiobras.value = False
    elif (estado == "Equilibrio dos patas derecha"):
        ledManiobras.value = True
        maniobraInclinadoDerecha()
        time.sleep(1)
        ledManiobras.value = False
    elif (estado == "Ingreso manual de puntos"):
        ledManual.value = True
        puntosManual()
        time.sleep(1)
        ledManual.value = False
    elif (estado == "Marcha doble"):
        ledMarchas.value = True
        distance1 = medir_distancia(1)
        distance2 = medir_distancia(2)
        print(distance1, distance2)
        home()
        if distance1 < 25.0 or distance2 < 25.0:
            cambioHome()
        else:
            marchaDoble()
        ledMarchas.value = False
    elif (estado == "Marcha sencilla"):
        ledMarchas.value = True
        distance1 = medir_distancia(1)
        distance2 = medir_distancia(2)
        print(distance1, distance2)
        home()
        if distance1 < 25.0 or distance2 < 25.0:
            cambioHome()
        else:
            marchaSencilla()
        ledMarchas.value = False
