import busio
import board
import analogio
import digitalio
import json
import socketpool
import ssl
import time
import wifi
import adafruit_requests as requests
import wifi_networks

def connection():
    print("INICIO")
    wifi_networks.connect()
    print("FIN")
connection()

azure = "https://tg-backend-jl.azurewebsites.net/api/GuardarAngulos"
webhook = "https://webhook.site/fa02fa4d-43ee-4595-bb87-a56ef514b6b9"
pool = socketpool.SocketPool(wifi.radio)
https = requests.Session(pool, ssl.create_default_context())

uart = busio.UART(board.TX, board.RX, baudrate=9600)

# Configurar el pin analógico
entrada_34 = board.D34
entrada_35 = board.D35
# Crear un objeto de entrada analógica
M7 = analogio.AnalogIn(entrada_34)
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
    if uart.in_waiting > 0:
        data = uart.readline().decode().strip()
        try:
            json_data = json.loads(data)
            voltages = voltage(json_data)
            #print("Voltajes:", voltages)
            grados = deg(voltages)
            #print("Grados:", grados)
            
            valor_analogico_M7 = M7.value
            valor_analogico_M8 = M8.value
            
            json_data['A41'] = valor_analogico_M7
            json_data['A42'] = valor_analogico_M8
            
            voltages['A41'] = valor_analogico_M7 * (3.3 / 65535)
            voltages['A42'] = valor_analogico_M8 * (3.3 / 65535)
            
            grados['A41'] = int((voltages['A41'] -0.437499999)/0.0144166667)
            grados['A42'] = int((voltages['A42'] -0.437499999)/0.0144166667)
            
            print("AnalogRead", json_data)
            print("Voltajes:", voltages)
            print("Grados:", grados)
            
            print("POSTing data to {0}".format(azure))
            response = https.post(azure, data=str(grados))
            json_resp = response
            response.close()
            
            print('=============================================')
        except ValueError:
            print("Error al decodificar el JSON")