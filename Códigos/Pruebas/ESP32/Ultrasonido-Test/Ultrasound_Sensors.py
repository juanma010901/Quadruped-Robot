import time
import board
import pulseio
import adafruit_hcsr04

# Configurar los pines Trig y Echo del sensor de ultrasonido
echo_pin1 = board.D34
echo_pin2 = board.D35
trig_pin1 = board.D32
trig_pin2 = board.D33

# Configurar el temporizador para medir la duración del pulso de eco
timer1 = pulseio.PulseIn(echo_pin1, maxlen=1)
timer2 = pulseio.PulseIn(echo_pin2, maxlen=1)

# Configurar el objeto del sensor de ultrasonido
sonar1 = adafruit_hcsr04.HCSR04(trigger_pin=trig_pin1, echo_pin=echo_pin1, timeout=0.1)
sonar2 = adafruit_hcsr04.HCSR04(trigger_pin=trig_pin2, echo_pin=echo_pin2, timeout=0.1)

# Definir la función de medición de distancia
def medir_distancia(sensor):
    try:
        if sensor == 1:
            distance1 = sonar1.distance
            return distance1
        elif sensor == 2:
            distance2 = sonar2.distance
            return distance2
    except:
        if sensor == 1:
            distance1 = 450
            return distance1
        elif sensor == 2:
            distance2 = 450
            return distance2

while True:
    # Llamar a la función de medición de distancia
    distance1 = medir_distancia(1)
    distance2 = medir_distancia(2)
    
    print("Distancia 1:", distance1, "cm")
    print("Distancia 2:", distance2, "cm")
        
    # Esperar un momento antes de volver a medir la distancia
    time.sleep(0.1)
