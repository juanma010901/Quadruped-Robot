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

#MQTT
broker = 'io.adafruit.com'
port = 1883
ssid = "Redmi"
password = "987654321"
#ssid = "Test"
#password = "12345678"
aio_username = secrets.secrets["aio_username"]
aio_key = secrets.secrets["aio_key"]

#REALTIME DATABASE
#firebase = "https://esp32-2952e-default-rtdb.firebaseio.com/"
azure = "https://masterusers.azurewebsites.net/api/GetMotion"

# Configura los LEDs
ledMS = digitalio.DigitalInOut(board.D32)
ledMS.direction = digitalio.Direction.OUTPUT
ledMD = digitalio.DigitalInOut(board.D33)
ledMD.direction = digitalio.Direction.OUTPUT

wifi.radio.connect(ssid, password)
print("Connected to %s!" % ssid)
print("My IP address is", wifi.radio.ipv4_address)

mqtt_MarchaSencilla = aio_username + '/feeds/MarchaSencilla'
mqtt_MarchaDoble = aio_username + '/feeds/MarchaDoble'
mqtt_home = aio_username + '/feeds/Home'

pool = socketpool.SocketPool(wifi.radio)
https = requests.Session(pool, ssl.create_default_context())

mqtt = MQTT.MQTT(
    broker=broker,
    port=port,
    username=aio_username,
    password=aio_key,
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

switch_marchaSencilla = False
switch_marchaDoble = False

def message(client, topic, message):
    # Method called when a client's subscribed feed has a new value.
    print(client, topic, message)
    global switch_marchaSencilla
    global switch_marchaDoble
    if(topic == mqtt_MarchaSencilla and message == "ON"):
        switch_marchaDoble = False
        mqtt.publish(mqtt_MarchaDoble, "OFF")
        ledMS.value = True
        switch_marchaSencilla = True
    elif(topic == mqtt_MarchaSencilla and message == "OFF"):
        ledMS.value = False
        switch_marchaSencilla = False
    if(topic == mqtt_MarchaDoble and message == "ON"):
        switch_marchaSencilla = False
        mqtt.publish(mqtt_MarchaSencilla, "OFF")
        ledMD.value = True
        switch_marchaDoble = True
    elif(topic == mqtt_MarchaDoble and message == "OFF"):
        ledMD.value = False   
        switch_marchaDoble = False
         
    
    
    #print(switch_marcha)    

#Callbacks
mqtt.on_message = message
mqtt.connect()
mqtt.subscribe(mqtt_MarchaSencilla)
mqtt.subscribe(mqtt_MarchaDoble)
#mqtt.subscribe(mqtt_home)

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

# Configurar el pin 0,4 como entrada analógica
pin_adc1 = analogio.AnalogIn(board.D34)
pin_adc2 = analogio.AnalogIn(board.D35)
pin_adc3 = analogio.AnalogIn(board.D2)
pin_adc4 = analogio.AnalogIn(board.D25)
pin_adc5 = analogio.AnalogIn(board.D12)
pin_adc6 = analogio.AnalogIn(board.D26)
pin_adc7 = analogio.AnalogIn(board.D27)
pin_adc8 = analogio.AnalogIn(board.D13)

# Definir las longitudes de las dos articulaciones del robot
l1 = 11
l2 = 13

#---------------------------------------------------------------------------------

#Definición de los puntos a alcanzar para cada lado del robot
def puntosIzquierda():
    x = [2, 4, 0]
    y = [13, 14, 14]
    return ([x, y])

def puntosDerecha():
    x = [2, 0, 4]
    y = [13, 14, 14]
    return ([x, y])

def puntosHome():
    puntosIzquierda = [0, 14]
    puntosDerecha = [4, 14]
    return([puntosIzquierda, puntosDerecha])
    

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
    puntos = puntosIzquierda()
    x = puntos[0]
    y = puntos[1]

    angulosP1 = []

    for i in range(len(x)):
        angulosP1.append(inversaIzquierda(x[i],y[i]))
    return angulosP1

# Mover Pata 2 (izquierda)
def calcularAngulosP2():
    #Definir los vectores x e y
    puntos = puntosIzquierda()
    x = puntos[0]
    y = puntos[1]

    angulosP2 = []

    for i in range(len(x)):
        angulosP2.append(inversaIzquierda(x[i],y[i]))
    return angulosP2
    
# Mover Pata 3 (derecha)
def calcularAngulosP3():
    #Definir los vectores x e y
    puntos = puntosDerecha()
    x = puntos[0]
    y = puntos[1]

    angulosP3 = []

    for i in range(len(x)):
        angulosP3.append(inversaDerecha(x[i],y[i]))
    return angulosP3

# Mover Pata 4 (derecha)
def calcularAngulosP4():
    puntos = puntosDerecha()
    x = puntos[0]
    y = puntos[1]

    angulosP4 = []

    for i in range(len(x)):
        angulosP4.append(inversaDerecha(x[i],y[i]))
    return angulosP4

#---------------------------------------------------------------------------------

#Leer ADC's e imprimir voltajes
def leerVoltaje(pata):
    
    if pata == 1:
        #Leer el valor del voltaje en el pin (en milivoltios)
        voltajeUp = pin_adc1.value * 3.3 / 65535.0
        voltajeDown = pin_adc2.value * 3.3 / 65535.0
        #Linezalización del voltaje para conocer los grados, según ecuación hallada
        gradosUp = (((voltajeUp-0.437999999)/0.0144166667))
        gradosDown = (((voltajeDown-0.437999999)/0.0144166667))
        
        #print("Fetching text from %s" % firebase+"/Potenciometros.json")
        datos = {"P1U": gradosUp, "P1D": gradosDown}
        #response = https.put(firebase+"/Potenciometros.json", json=datos)
        #response.close()
    
    elif pata == 2:
        #Leer el valor del voltaje en el pin (en milivoltios)
        voltajeUp = pin_adc1.value * 3.3 / 65535.0
        voltajeDown = pin_adc2.value * 3.3 / 65535.0
        #Linezalización del voltaje para conocer los grados, según ecuación hallada
        gradosUp = (((voltajeUp-0.437999999)/0.0144166667))
        gradosDown = (((voltajeDown-0.437999999)/0.0144166667))
        
        #print("Fetching text from %s" % firebase+"/Potenciometros.json")
        datos = {"P2U": gradosUp, "P2D": gradosDown}
        #response = https.put(firebase+"/Potenciometros.json", json=datos)
        #response.close()
        
    elif pata == 3:
        # Leer el valor del voltaje en el pin (en milivoltios)
        voltajeUp = pin_adc1.value * 3.3 / 65535.0
        voltajeDown = pin_adc2.value * 3.3 / 65535.0
        #Linezalización del voltaje para conocer los grados, según ecuación hallada
        gradosUp = (((voltajeUp-0.437999999)/0.0144166667))
        gradosDown = (((voltajeDown-0.437999999)/0.0144166667))
        
        #print("Fetching text from %s" % firebase+"/Potenciometros.json")
        datos = {"P3U": gradosUp, "P3D": gradosDown}
        #response = https.put(firebase+"/Potenciometros.json", json=datos)
        #response.close()
        
    elif pata == 4:
        # Leer el valor del voltaje en el pin (en milivoltios)
        voltajeUp = pin_adc1.value * 3.3 / 65535.0
        voltajeDown = pin_adc2.value * 3.3 / 65535.0
        #Linezalización del voltaje para conocer los grados, según ecuación hallada
        gradosUp = (((voltajeUp-0.437999999)/0.0144166667))
        gradosDown = (((voltajeDown-0.437999999)/0.0144166667))
        
        #print("Fetching text from %s" % firebase+"/Potenciometros.json")
        datos = {"P4U": gradosUp, "P4D": gradosDown}
        #response = https.put(firebase+"/Potenciometros.json", json=datos)
        #response.close()

    return([voltajeUp, voltajeDown, gradosUp, gradosDown])

#---------------------------------------------------------------------------------

#Funciones para mover las patas e imprimir la información
def moverP1(puntosP1):
    for i in range(len(puntosP1)):
            servo_1.angle = puntosP1[i][0]
            servo_2.angle = puntosP1[i][1]
            time.sleep(0.5)
            
            #Medir Valores de ADC's
            #(VTC: Valores Teóricos Corregidos)
            #(VE: Valores Experimentales)
            adc = leerVoltaje(1)
            print("Pata1: ", adc[0], adc[1], "V.T.C: ", puntosP1[i][0], puntosP1[i][1], "V.E: ", adc[2]-5, adc[3]+5)
            
def moverP2(puntosP2):
    for i in range(len(puntosP2)):
            servo_3.angle = puntosP2[i][0]
            servo_4.angle = puntosP2[i][1]
            time.sleep(0.5)
            
            #Medir Valores de ADC's
            #(VTC: Valores Teóricos Corregidos)
            #(VE: Valores Experimentales)
            adc = leerVoltaje(2)
            print("Pata2: ", adc[0], adc[1], "V.T.C: ", puntosP2[i][0], puntosP2[i][1], "V.E: ", adc[2], adc[3])
            
def moverP3(puntosP3):
    for i in range(len(puntosP3)):
            servo_5.angle = puntosP3[i][0]
            servo_6.angle = puntosP3[i][1]
            time.sleep(0.5)
            
            #Medir Valores de ADC's
            #(VTC: Valores Teóricos Corregidos)
            #(VE: Valores Experimentales)
            adc = leerVoltaje(3)
            print("Pata3: ", adc[0], adc[1], "V.T.C: ", puntosP3[i][0], puntosP3[i][1], "V.E: ", adc[2], adc[3])
            
def moverP4(puntosP4):
    for i in range(len(puntosP4)):
            servo_7.angle = puntosP4[i][0]
            servo_8.angle = puntosP4[i][1]
            time.sleep(0.5)
            
            #Medir Valores de ADC's
            #(VTC: Valores Teóricos Corregidos)
            #(VE: Valores Experimentales)
            adc = leerVoltaje(4)
            print("Pata4: ", adc[0], adc[1], "V.T.C: ", puntosP4[i][0], puntosP4[i][1], "V.E: ", adc[2], adc[3])

#---------------------------------------------------------------------------------
            
def moverP1P3(puntosP1, puntosP3):
    for i in range(len(puntosP1)):
            servo_1.angle = puntosP1[i][0]
            servo_2.angle = puntosP1[i][1]
            servo_5.angle = puntosP3[i][0]
            servo_6.angle = puntosP3[i][1]
            time.sleep(0.3)
            
            #Medir Valores de ADC's
            #(VTC: Valores Teóricos Corregidos)
            #(VE: Valores Experimentales)
            adc1 = leerVoltaje(1)
            adc2 = leerVoltaje(3)
            print("Pata1: ", adc1[0], adc1[1], "V.T.C: ", puntosP1[i][0], puntosP1[i][1], "V.E: ", adc1[2], adc1[3])
            print("Pata3: ", adc2[0], adc2[1], "V.T.C: ", puntosP3[i][0], puntosP3[i][1], "V.E: ", adc2[2], adc2[3])
            
def moverP2P4(puntosP2, puntosP4):
    for i in range(len(puntosP2)):
            servo_3.angle = puntosP2[i][0]
            servo_4.angle = puntosP2[i][1]
            servo_7.angle = puntosP4[i][0]
            servo_8.angle = puntosP4[i][1]
            time.sleep(0.3)
            
            #Medir Valores de ADC's
            #(VTC: Valores Teóricos Corregidos)
            #(VE: Valores Experimentales)
            adc1 = leerVoltaje(2)
            adc2 = leerVoltaje(4)
            print("Pata2: ", adc1[0], adc1[1], "V.T.C: ", puntosP2[i][0], puntosP2[i][1], "V.E: ", adc1[2], adc1[3])
            print("Pata4: ", adc2[0], adc2[1], "V.T.C: ", puntosP4[i][0], puntosP4[i][1], "V.E: ", adc2[2], adc2[3])
            
#---------------------------------------------------------------------------------


#Definición del Home (correr postura inicial)
def home():
    global switch_home
    home = puntosHome()
    servo_3.angle, servo_4.angle = inversaIzquierda(home[0][0], home[0][1])
    servo_5.angle, servo_6.angle = inversaDerecha(home[1][0], home[1][1])
    time.sleep(0.1)
    servo_1.angle, servo_2.angle = inversaIzquierda(home[0][0], home[0][1])
    servo_7.angle, servo_8.angle = inversaDerecha(home[1][0], home[1][1])
            
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

#Llamar al home
home()

while True:
    print("Fetching text from %s" % azure)
    response = https.get(azure)
    print(response.json())
    start = response.json()["start"]
    TrackId = response.json()["trackId"]
    print(response.json())
    response.close()
    #time.sleep(1)

    #Llamar a la marcha que va a hacer el robot
    #mqtt.loop()
    if switch_marchaSencilla or TrackId == 1:
        marchaSencilla()
    elif switch_marchaDoble or TrackId == 2:
        marchaDoble()
    #else:
        #home()
    #time.sleep(1)
    
