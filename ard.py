import serial
import serial.tools.list_ports as list_ports
from using_vpn import get_user_ip

_IP = get_user_ip()

print(_IP)

def send_ard(password):
    try:
        ard_port = None
        for port,title,*_ in map(tuple, list_ports.comports()):
            if 'arduino' in title.lower():
                ard_port = port
                break
        if ard_port is None:
            raise ConnectionAbortedError()
        arduino = serial.Serial(ard_port, 115200)
    except:
        raise ConnectionRefusedError()
    data = f'{_IP},{password}'
    arduino.write(data.encode())
    arduino.close()

