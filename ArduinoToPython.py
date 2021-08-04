from ctypes import string_at
import serial
import time

# Makes connection to the arduino
arduino = serial.Serial(port='COM4', baudrate=115200)
arduino.timeout = 1

# Sends new position and receives the new position the motors are set to.
def write_read(x):
    arduino.write(x)
    time.sleep(0.1)
    data = arduino.readline().decode('ascii')
    return data

# Converts a string into a byte array.
def toByteArray(m):
    encoded_string = m.encode()
    byt_array = bytearray(encoded_string)
    return byt_array


def getPosition(position_x, position_y):
    position = str(position_x) + "," + str(position_y)
    BytePosition = toByteArray(position)
    value = write_read(BytePosition)
    print("Arduino say: " + str(value))
