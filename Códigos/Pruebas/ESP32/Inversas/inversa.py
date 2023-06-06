import math

# Definir las longitudes de las dos articulaciones del robot
l1 = 11
l2 = 13

# Definir las coordenadas del punto final
x = 0
y = 24

# Calcular el valor de theta 2
theta2 = math.acos((x**2 + y**2 - l1**2 - l2**2) / (2*l1*l2))

# Calcular el valor de theta 1
theta1 = math.atan2(y, x) - math.atan2(l2*math.sin(theta2), l1+l2*math.cos(theta2))

# Imprimir los valores de theta 1 y theta 2 en grados y radianes
print("Theta 1: ", math.degrees(theta1), "grados")
print("Theta 2: ", math.degrees(theta2), "grados")
