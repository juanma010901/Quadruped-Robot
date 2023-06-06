import busio
import board
import analogio
import digitalio
import json
import ssl
import time
import wifi
import wifi_networks

import socketpool
import adafruit_requests as requests

#import socket
#import adafruit_requests


def connection():
    print("INICIO")
    wifi_networks.connect()
    print("FIN")
connection()

azure = "https://tg-backend-jl.azurewebsites.net/api/GuardarAngulos"
webhook = "https://webhook.site/60b6863b-6f1a-4d13-819b-a33a30a78183"

#http = adafruit_requests.Session(socket)

#pool = socketpool.SocketPool(wifi.radio)
#https = requests.Session(pool, ssl.create_default_context())

pool = socketpool.SocketPool(wifi.radio)
context = ssl.create_default_context()
context.check_hostname = False
https = requests.Session(pool, context)

uart = busio.UART(board.TX, board.RX, baudrate=9600)

# Configurar el pin analógico
entrada_34 = board.D34
entrada_35 = board.D35
# Crear un objeto de entrada analógica
M6 = analogio.AnalogIn(entrada_34)
M8 = analogio.AnalogIn(entrada_35)

def voltage(json_data):
    voltage_dic = {}
    for c,v in json_data.items():
         voltage_dic[c] = v * (5.0 / 1023)
    #voltage_dic = sorted(voltage_dic.keys())
    return voltage_dic
    
def deg(voltages):
    deg_dic = {}
    for c,v in voltages.items():
         deg_dic[c] = int((v-0.437499999)/0.0144166667)
    return deg_dic

while True:
    if uart.in_waiting > 0 and wifi.radio.ipv4_address:
        data = uart.readline().decode().strip()
        try:
            json_data = json.loads(data)
            voltages = voltage(json_data)
            #print("Voltajes:", voltages)
            grados = deg(voltages)
            #print("Grados:", grados)
            
            valor_analogico_M6 = M6.value
            valor_analogico_M8 = M8.value
            
            json_data['A32'] = valor_analogico_M6
            json_data['A42'] = valor_analogico_M8
            
            voltages['A32'] = valor_analogico_M6 * (3.3 / 65535)
            voltages['A42'] = valor_analogico_M8 * (3.3 / 65535)
            
            grados['A32'] = int((voltages['A32'] -0.437499999)/0.0144166667)
            grados['A42'] = int((voltages['A42'] -0.437499999)/0.0144166667)
            
            print("AnalogRead", json_data)
            print("Voltajes:", voltages)
            print("Grados:", grados)
            
            print("POSTing data to {0}".format(azure))
            
            #azure
            #webhook
            
            response = https.post(azure, data=str(grados))
            #json_resp = response.json()
            #print("Data received from server:", json_resp["data"])
            response.close()
            
            #response = http.post(webhook, data=str(grados))
            #response.close()
                        
            print('=============================================================================================================')
        except ValueError:
            print("Error al decodificar el JSON")
            #connection()
            
            
            
            