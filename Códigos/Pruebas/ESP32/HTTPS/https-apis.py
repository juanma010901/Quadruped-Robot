#from firebase import firebase
import ssl
import wifi
import socketpool
import json

import adafruit_requests as requests


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to %s" % secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!" % secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

socket = socketpool.SocketPool(wifi.radio)
https = requests.Session(socket, ssl.create_default_context())

#TEXT_URL = "https://httpbin.org/get"
TEXT_URL = "https://randomuser.me/api/"
JSON_GET_URL = "https://httpbin.org/get"
JSON_POST_URL = "https://httpbin.org/post"

firebase = "https://esp32-2952e-default-rtdb.firebaseio.com/"
print("Fetching text from %s" % firebase+"Potenciometros.json")
datos = {"dato": "Hola, mundo, qué tal?!"}
response = https.put(firebase+"Potenciometros.json", json=datos)
response.close()

firebase = "https://esp32-2952e-default-rtdb.firebaseio.com/Sensores.json"
print("Fetching text from %s" % firebase)
response = https.get(firebase)
print(response.json())
response.close()

#print("Fetching text from %s" % TEXT_URL)
#response = https.get(TEXT_URL)
#print("-" * 40)
#print("Text Response: ", response.text)
#print("-" * 40)
#response.close()

#print("Fetching JSON data from %s" % JSON_GET_URL)
#response = https.get(JSON_GET_URL)
#print("-" * 40)

#print("JSON Response: ", response.json())
#print("-" * 40)

#data = "31F"
#print("POSTing data to {0}: {1}".format(JSON_POST_URL, data))
#response = https.post(JSON_POST_URL, data=data)
#print("-" * 40)

#json_resp = response.json()
# Parse out the 'data' key from json_resp dict.
#print("Data received from server:", json_resp["data"])
#print("-" * 40)

#json_data = {"Date": "July 25, 2019"}
#print("POSTing data to {0}: {1}".format(JSON_POST_URL, json_data))
#response = https.post(JSON_POST_URL, json=json_data)
#print("-" * 40)

#json_resp = response.json()
# Parse out the 'json' key from json_resp dict.
#print("JSON Data received from server:", json_resp["json"])
#print("-" * 40)