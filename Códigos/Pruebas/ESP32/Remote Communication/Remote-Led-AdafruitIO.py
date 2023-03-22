import ssl
import socketpool
import wifi
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import board
import digitalio
import time
import secrets

#led = digitalio.DigitalInOut(board.D0)
#led.direction = digitalio.Direction.OUTPUT
#led.value = True

broker = 'io.adafruit.com'
port = 1883
ssid = secrets.secrets["ssid"]
password = secrets.secrets["password"]
aio_username = secrets.secrets["aio_username"]
aio_key = secrets.secrets["aio_key"]

# Configura el LED
led = digitalio.DigitalInOut(board.D32)
led.direction = digitalio.Direction.OUTPUT

wifi.radio.connect(ssid, password)
print("Connected to %s!" % ssid)

mqtt_led = aio_username + '/feeds/Led'
mqtt_slider = aio_username + '/feeds/Slider'
mqtt_motor1 = aio_username + '/feeds/Motor1'

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
    print(client, topic, message)
    if(topic == mqtt_led and message == "ON"):
        led.value = True
    elif(topic == mqtt_led and message == "OFF"):
        led.value = False
    elif(topic == mqtt_slider):
        print(message)
        mqtt.publish(mqtt_motor1, message)
    #print(LED)    

#Callbacks
mqtt.on_message = message

mqtt.connect()
mqtt.subscribe(mqtt_led)
mqtt.subscribe(mqtt_slider)


while True:
    mqtt.loop()
    time.sleep(1)
    

