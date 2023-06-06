import adafruit_pca9685
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import analogio
import board
import busio
import digitalio
import ipaddress
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

#Set static IP address
ipv4 =  ipaddress.IPv4Address("192.168.1.11")
netmask =  ipaddress.IPv4Address("255.255.255.0")
gateway =  ipaddress.IPv4Address("192.168.1.1")
wifi.radio.set_ipv4_address(ipv4=ipv4,netmask=netmask,gateway=gateway)
wifi.radio.connect(ssid, password)

print("Connected to %s!" % ssid)
print("My IP address is", wifi.radio.ipv4_address)