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
import secrets
import socketpool
import ssl
import time
import wifi
from adafruit_motor import servo

ssid = secrets.secrets["ssid"]
password = secrets.secrets["password"]
#ssid = "Redmi"
#password = "987654321"
#aio_username = secrets.secrets["aio_username"]
#aio_key = secrets.secrets["aio_key"]

#EndPoints API
getPuntos = "https://masterusers.azurewebsites.net/api/GetPuntos"
getModo = "https://masterusers.azurewebsites.net/api/GetModoActual"
updateModo = "https://masterusers.azurewebsites.net/api/ActualizarModo"

#Set static IP address
# ipv4 =  ipaddress.IPv4Address("192.168.1.3")
# netmask =  ipaddress.IPv4Address("255.255.255.0")
# gateway =  ipaddress.IPv4Address("192.168.1.1")
# wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
wifi.radio.connect(ssid, password)

print("Connected to %s!" % ssid)
print("My IP address is", wifi.radio.ipv4_address)

pool = socketpool.SocketPool(wifi.radio)
https = requests.Session(pool, ssl.create_default_context())

data = '{"Id":1,"Activo": true,"Descripcion": "Home","SeccionId": 1}'
print("POSTing data to {0}: {1}".format(updateModo, data))
response = https.put(updateModo, data=data)
