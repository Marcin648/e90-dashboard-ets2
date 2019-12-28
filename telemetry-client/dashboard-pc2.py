import serial
import time
import struct

import pcars
from pcars.stream import PCarsStreamReceiver

serialPort = 'COM3'
serialBaudrate = 115200

ser = serial.Serial(port=serialPort, baudrate=serialBaudrate);
ser.reset_input_buffer()

a = []
class MyPCarsListener(object):
    def handlePacket(self, data):
        global a
        a = data

        if(not type(data) is pcars.packet.TelemetryPacket):
            return

        packet = bytearray()
        packet += b'Q'

        packet += (1 if data['rpm'] > 0 else 0).to_bytes(1, 'little') #engineOn

        packet += (1).to_bytes(1, 'little') #lightsParkingOn
        packet += (0).to_bytes(1, 'little') #lightsBeamLowOn
        packet += (0).to_bytes(1, 'little') #lightsBeamHighOn
        packet += (0).to_bytes(1, 'little') #fogLight

        packet += (0).to_bytes(1, 'little') #blinkers

        packet += (int(data["brake"]/255)).to_bytes(1, 'little') #parking brake

        packet += int(data["rpm"]).to_bytes(2, 'little')
        packet += int(abs(data["speed"]*3.6)).to_bytes(2, 'little')

        fuel = int((data['fuelLevel'])*1000)
        packet += fuel.to_bytes(2, 'little')

        packet += (16).to_bytes(1, 'little')
        packet += (0).to_bytes(1, 'little')
        packet += (0).to_bytes(1, 'little')

        packet += (2).to_bytes(1, 'little')
        packet += (7).to_bytes(1, 'little')

        packet += (2019).to_bytes(2, 'little')

        ser.write(packet)
        ser.reset_input_buffer()


if ser.is_open:
    listener = MyPCarsListener()
    stream = PCarsStreamReceiver()
    stream.addListener(listener)
    stream.start()

while ser.is_open:
    time.sleep(1)

print("Serial connection closed")
