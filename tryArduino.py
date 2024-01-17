import serial
import time

# Change the port to '/dev/ttyACM0'
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Rest of the code remains the same
try:
    while True:
        try:
            input_data = arduino.readline().decode('ISO-8859-1').strip()
        except UnicodeDecodeError:
            input_data = arduino.readline().decode('utf-8').strip()

        if input_data.lower() in ['f', 'fade', 'up', 'down']:
            fade_up()
        elif input_data.lower() in ['l', 'left', 'right']:
            fade_left()
        else:
            print("Unknown command:", input_data)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

