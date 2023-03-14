import time
import board
import pwmio
from adafruit_motor import servo

# Configurar el pin 27 como una salida PWM
pwm = pwmio.PWMOut(board.D5, duty_cycle=2 ** 15, frequency=50)

# Crear un objeto servo
servo = servo.Servo(pwm, min_pulse=500, max_pulse=2500)

# Mover el servo a 0 grados
servo.angle = 0
time.sleep(1)

# Mover el servo a 90 grados
servo.angle = 90
time.sleep(1)

# Mover el servo a 180 grados
servo.angle = 180
time.sleep(1)

# Detener el servo en su posición actual
servo.throttle = None

