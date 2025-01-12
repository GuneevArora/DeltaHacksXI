import serial
import time
from using_vpn import get_user_ip

_IP = None
_PASS = None

def send_ard(password):
    arduino = serial.Serial('COM3', 115200)  
    time.sleep(2) 


    _PASS = password


    # Combine password and IP address into a single string
    data = f"{_PASS},{_IP}"

    # Send the data over serial
    arduino.write(data.encode())

    # Print the data sent to confirm
    print(f"Sent data: {data}")

    arduino.close()  # Close the serial connection

def send_ard(ip_address):
    arduino = serial.Serial('COM3', 115200)  
    time.sleep(2) 


    password = "No data"
    ip_address = get_user_ip()  

    # Combine password and IP address into a single string
    data = f"{_PASS},{ip_address}"

    # Send the data over serial
    arduino.write(data.encode())

    # Print the data sent to confirm
    print(f"Sent data: {data}")

    arduino.close()  # Close the serial connection


    