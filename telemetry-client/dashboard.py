import serial
import requests
import time
import dateutil.parser
from cobs import cobs

serialPort = 'COM4'
serialBaudrate = 115200

telemetryServer = "http://127.0.0.1:25555/api/ets2/telemetry"
#telemetryServer = "http://10.8.0.3:25555/api/ets2/telemetry"

ser = serial.Serial(port=serialPort, baudrate=serialBaudrate, timeout=0.5)

ser.flushInput()
while ser.is_open:
    telemetry = requests.get(telemetryServer).json()
    truck = telemetry["truck"]
    packet = bytearray()

    packet += truck["engineOn"].to_bytes(1, 'little')
    packet += truck["lightsParkingOn"].to_bytes(1, 'little')
    packet += truck["lightsBeamLowOn"].to_bytes(1, 'little')
    packet += truck["lightsBeamHighOn"].to_bytes(1, 'little')

    fogLight = truck["lightsAuxFrontOn"] or truck["lightsAuxFrontOn"]
    packet += fogLight.to_bytes(1, 'little')

    if truck["blinkerLeftOn"] and truck["blinkerRightOn"]:
        packet += (3).to_bytes(1, 'little')
    else:
        if truck["blinkerLeftActive"]:
            packet += (1).to_bytes(1, 'little')
        elif truck["blinkerRightActive"]:
            packet += (2).to_bytes(1, 'little')
        else:
            packet += (0).to_bytes(1, 'little')

    packet += truck["parkBrakeOn"].to_bytes(1, 'little')

    packet += int(truck["engineRpm"]).to_bytes(2, 'little')
    packet += int(abs(truck["speed"])).to_bytes(2, 'little')

    fuel = 0
    if truck["fuelCapacity"] > 0:
        fuel = int((truck["fuel"]/truck["fuelCapacity"])*1000)

    packet += fuel.to_bytes(2, 'little')

    gameTime = dateutil.parser.parse(telemetry["game"]["time"])

    packet += gameTime.hour.to_bytes(1, 'little')
    packet += gameTime.minute.to_bytes(1, 'little')
    packet += gameTime.second.to_bytes(1, 'little')

    packet += gameTime.day.to_bytes(1, 'little')
    packet += gameTime.month.to_bytes(1, 'little')

    packet += gameTime.year.to_bytes(2, 'little')

    encoded = cobs.encode(packet) + b'\x00'
    ser.write(encoded)
    time.sleep(0.01)

print("Serial connection closed")
