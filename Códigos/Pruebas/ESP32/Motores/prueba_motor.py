import time
import board
import pwmio
from adafruit_motor import servo

# Configurar el pin 32 como una salida PWM
pwm = pwmio.PWMOut(board.D32, duty_cycle=2 ** 15, frequency=50)

# Crear un objeto servo
servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

while True:
    
    # Mover el servo
    grados = int(input("Ingrese el ángulo: "))
    servo.angle = grados

#CODIGO FUNCIONANDO CORRECTAMENTE
