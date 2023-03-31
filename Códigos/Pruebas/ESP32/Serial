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

ssid = "Redmi"
password = "987654321"
wifi.radio.connect(ssid, password)
print("Connected to %s!" % ssid)
print("My IP address is", wifi.radio.ipv4_address)

azure = "https://masterusers.azurewebsites.net/api/UpdateMotion"
pool = socketpool.SocketPool(wifi.radio)
https = requests.Session(pool, ssl.create_default_context())

uart = busio.UART(board.TX, board.RX, baudrate=9600)

while True:
    data = uart.read(32)  # read up to 32 bytes
    # print(data)  # this is a bytearray type

    if data is not None:
        # convert bytearray to string
        data_string = ''.join([chr(b) for b in data])
        #print(data_string, end="")
        
        # String en formato JSON
        json_string = '"' + data_string + '"'
        # Carga el string JSON en un objeto Python
        json_obj = json.loads(json_string)
        
        json = json_obj.json()
        
        # Imprime el objeto JSON
        print(json, end="")
        
        #json_data = {"Date": "July 25, 2019"}
        #print("Fetching text from %s" % azure)
        #response = https.put(azure, data={"id":1,"start":False,"trackId":2})
        #response.close()
        
        
