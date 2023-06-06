import adafruit_requests as requests
import board
import busio
import time
import wifi
from secrets import redes 

banderaConnected = False

def connect_to_network():
    global banderaConnected
    for red in redes:
        try:
            print("Conectando a ", red['ssid'])
            wifi.radio.connect(red['ssid'], red['password'])
            print("Conectado a la red ", red['ssid'])
            print("Dirección IP: ", wifi.radio.ipv4_address)
            #print(banderaConnected)
            banderaConnected = True
            #print(banderaConnected)
            break
        except Exception as e:
            print("Error al conectar a ", red['ssid'], ": ", e)
            print("Dirección IP: ", wifi.radio.ipv4_address)
            banderaConnected = False
            #print(banderaConnected)

def connect():
    global banderaConnected
    while banderaConnected != True:
        connect_to_network()
        print("Fin funcion", banderaConnected)
    banderaConnected = False
            
#connect()