import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import board
from digitalio import DigitalInOut, Direction
import time
import secrets

broker = 'io.adafruit.com'
port = 1883
ssid = secrets.secrets["ssid"]
password = secrets.secrets["password"]
aio_username = secrets.secrets["aio_username"]
aio_key = secrets.secrets["aio_key"]

# Configura el LED
led = DigitalInOut(board.D32)
led.direction = Direction.OUTPUT

wifi.radio.connect(ssid, password)
print("Connected to %s!" % ssid)

mqtt_topic = aio_username + '/feeds/Led'

pool = socketpool.SocketPool(wifi.radio)

mqtt = MQTT.MQTT(
    broker=broker,
    port=port,
    username=aio_username,
    password=aio_key,
    socket_pool=pool,
    ssl_context=ssl.create_default_context(),
)

def message(client, topic, message):
    # Method called when a client's subscribed feed has a new value.
    #print(message)
    if(message == "ON"):
        led.value = True
    else:
        led.value = False
    #print(LED)    

#Callbacks
mqtt.on_message = message

mqtt.connect()
mqtt.subscribe(mqtt_topic)
#mqtt.publish(mqtt_topic, "ON")

while True:
    mqtt.loop()
    time.sleep(1)

