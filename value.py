import serial
import time

# Replace with the appropriate serial port for your system
# On Windows, it might be 'COMx', on Linux, it could be '/dev/ttyUSB0' or '/dev/ttyACM0'
ser = serial.Serial('COM3', 9600)  # Open the serial port (replace 'COMx' with your port)
time.sleep(2)  # Wait for the connection to establish


def read_sensor_data():
    
    while True:
        if ser.in_waiting > 0:  # Check if data is available to read
            sensor_value = ser.readline().decode('utf-8').strip()  # Read and decode the sensor data
            print(f"Sensor Value: {sensor_value}") 
            return sensor_value
            # Print the sensor value
