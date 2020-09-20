from serial import Serial
from cobs import cobs
import time
import threading

class Dashboard:
    BLINKERS_OFF = 0
    BLINKERS_LEFT = 1
    BLINKERS_RIGHT = 2
    BLINKERS_HAZZARD = 3

    def __init__(self):
        self.ignition = False
        self.parking_lights = False
        self.dipped_lights = False
        self.main_lights = False
        self.fog_lights = False
        self.blinkers = Dashboard.BLINKERS_OFF
        self.handbrake = False
        self.RPM = 0
        self.speed = 0
        self.fuel = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.day = 1
        self.month = 1
        self.year = 2019

        self.__serial = Serial()
        self.__lock = threading.Lock()

    def open(self, port = None, baudrate = 115200):
        self.__serial = Serial(port=port, baudrate=baudrate, timeout=1.0, write_timeout=2.0)
        time.sleep(1)
        self.__serial.flushInput()
        return self.__serial.isOpen()

    def close(self):
        self.__serial.close()

    def isOpen(self):
        return self.__serial.isOpen()

    def update(self):
        self.__lock.acquire()
        packet = bytearray()
        packet += self.ignition.to_bytes(1, 'little')
        packet += self.parking_lights.to_bytes(1, 'little')
        packet += self.dipped_lights.to_bytes(1, 'little')
        packet += self.main_lights.to_bytes(1, 'little')
        packet += self.fog_lights.to_bytes(1, 'little')
        packet += self.blinkers.to_bytes(1, 'little')
        packet += self.handbrake.to_bytes(1, 'little')
        packet += int(self.RPM).to_bytes(2, 'little')
        packet += int(abs(self.speed)).to_bytes(2, 'little')
        packet += int(self.fuel).to_bytes(2, 'little')
        packet += int(self.hour).to_bytes(1, 'little')
        packet += int(self.minute).to_bytes(1, 'little')
        packet += int(self.second).to_bytes(1, 'little')
        packet += int(self.day).to_bytes(1, 'little')
        packet += int(self.month).to_bytes(1, 'little')
        packet += int(self.year).to_bytes(2, 'little')
        self.__lock.release()
        packet_encoded = cobs.encode(packet) + b'\x00'
        self.__serial.write(packet_encoded)
        

    
