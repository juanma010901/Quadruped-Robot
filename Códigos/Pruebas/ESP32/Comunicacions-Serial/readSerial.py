import busio

uart = busio.UART(board.TX, board.RX, baudrate=9600)

while True:
    if uart.in_waiting > 0:
        data = uart.read(uart.in_waiting)
        print("Received data:", data.decode())
