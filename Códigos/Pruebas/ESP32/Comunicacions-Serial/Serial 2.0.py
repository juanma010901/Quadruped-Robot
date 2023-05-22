import busio
import digitalio
import json
import socketpool
import ssl
import time
import wifi
import adafruit_requests as requests

ssid = ""
password = ""
wifi.radio.connect(ssid, password)
print("Connected to %s!" % ssid)
print("My IP address is", wifi.radio.ipv4_address)

#azure = "https://masterusers.azurewebsites.net/api/UpdateMotion"
#azure = "https://masterusers.azurewebsites.net/api/GuardarPuntos"
azure = "https://webhook.site/fa02fa4d-43ee-4595-bb87-a56ef514b6b9"
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
        
        #json = json_obj.json()
        
        # Imprime el objeto JSON
        #print((json_obj))
        
        print("POSTing data to {0}: {1}".format(azure, json_obj))
        response = https.post(azure, data=json_obj)
        print("-" * 40)

        #json_resp = response
        # Parse out the 'data' key from json_resp dict.
        #print("Data received from server:", json_resp)
        #print("-" * 40)
        response.close()
        
        time.sleep(1)
        

        
        