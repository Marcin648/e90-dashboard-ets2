import serial
import socket
import time
import struct

serialPort = 'COM3'
serialBaudrate = 115200

ser = serial.Serial(port=serialPort, baudrate=serialBaudrate);
ser.flushInput()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('127.0.0.1', 20777)
sock.settimeout(1.0)
sock.bind(server_address)

d = b''
print()
while ser.is_open:
    try:
        data, address = sock.recvfrom(4096)
    except socket.timeout:
        continue

    if(len(data) < 152):
        print(len(data))
        continue

    telemetry = struct.unpack('27xf116xf', data[:152])

    print("%.5s %.5s" % telemetry, end='\r')

    speed = telemetry[0] * 3.6
    rpm = telemetry[1] * 10

    packet = bytearray()
    packet += b'Q'

    packet += (1).to_bytes(1, 'little')
    packet += (1).to_bytes(1, 'little')
    packet += (0).to_bytes(1, 'little')
    packet += (0).to_bytes(1, 'little')

    packet += (0).to_bytes(1, 'little')

    packet += (0).to_bytes(1, 'little')

    packet += (0).to_bytes(1, 'little')

    packet += int(rpm).to_bytes(2, 'little')
    packet += int(abs(speed)).to_bytes(2, 'little')

    packet += (5000).to_bytes(2, 'little')

    packet += (13).to_bytes(1, 'little')
    packet += (37).to_bytes(1, 'little')
    packet += (37).to_bytes(1, 'little')

    packet += (1).to_bytes(1, 'little')
    packet += (10).to_bytes(1, 'little')

    packet += (2019).to_bytes(2, 'little')

    ser.write(packet)
    ck = ser.read()


print("Serial connection closed")
