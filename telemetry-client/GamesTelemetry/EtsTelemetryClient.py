import socket
import struct
import time
from dataclasses import dataclass

TELE_TRUCK_WHEEL_COUNT = 10
TELE_TRAILER_WHEEL_COUNT = 18
TELE_TRAILER_COUNT = 10
TELE_STR_SIZE = 64

TELE_PACKET_COMMON = 0
TELE_PACKET_TRUCK = 1
TELE_PACKET_TRAILER = 2

TELE_PACKET_CONFIG_TRUCK = 100
TELE_PACKET_CONFIG_TRAILER = 101
TELE_PACKET_CONFIG_JOB = 102

TELE_PACKET_HEARTBEAT = 255

class DataStream:
    def __init__(self, data: bytearray, offset=0):
        self.offset = offset
        self.data = data

    def get(self, format_string):
        values = struct.unpack_from(format_string, self.data, offset=self.offset)
        self.offset += struct.calcsize(format_string)
        return values

    def getInt8(self):
        return self.get("<b")[0]

    def getUInt8(self):
        return self.get("<B")[0]

    def getInt16(self):
        return self.get("<h")[0]

    def getUInt16(self):
        return self.get("<H")[0]

    def getInt32(self):
        return self.get("<i")[0]

    def getUInt32(self):
        return self.get("<I")[0]

    def getInt64(self):
        return self.get("<q")[0]

    def getUInt64(self):
        return self.get("<Q")[0]

    def getFloat(self):
        return self.get("<f")[0]

    def getDouble(self):
        return self.get("<d")[0]

    def getVector(self):
        return Vector(*self.get("<fff"))

    def getEuler(self):
        return Euler(*self.get("<fff"))
    
    def getPlacement(self):
        placement = Placement()
        placement.position = self.getVector()
        placement.orientation = self.getEuler()
        return placement

    def getString(self, size):
        raw_string = bytearray(self.get("<" + str(size) + "B"))
        cstring = raw_string.decode().split("\x00")[0]
        return cstring


@dataclass
class Vector:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

@dataclass
class Euler:
    heading: float = 0.0
    pitch: float = 0.0
    roll: float = 0.0

@dataclass
class Placement:
    position: Vector = Vector()
    orientation: Euler = Euler()

@dataclass
class Common:
    game_paused: bool = False
    local_scale: float = 0.0
    game_time: int = 0
    next_rest_stop: int = 0

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        data_stream = DataStream(data, offset)
        common = Common()
        common.game_paused = data_stream.getUInt8()
        common.local_scale = data_stream.getFloat()
        common.game_time = data_stream.getUInt32()
        common.next_rest_stop = data_stream.getInt32()
        return common
        
@dataclass
class Truck():
    world_placement = Placement()
    local_linear_velocity = Vector()
    local_angular_velocity = Vector()
    local_linear_acceleration = Vector()
    local_angular_acceleration = Vector()
    cabin_offset = Placement()
    cabin_angular_velocity = Vector()
    cabin_angular_acceleration = Vector()
    head_offset = Placement()
    speed: float = 0.0
    engine_rpm: float = 0.0
    engine_gear: int = 0
    displayed_gear: int = 0
    input_steering: float = 0.0
    input_throttle: float = 0.0
    input_brake: float = 0.0
    input_clutch: float = 0.0
    effective_steering: float = 0.0
    effective_throttle: float = 0.0
    effective_brake: float = 0.0
    effective_clutch: float = 0.0
    cruise_control: float = 0.0
    hshifter_slot: int = 0
    parking_brake: int = 0
    motor_brake: int = 0
    retarder_level: int = 0
    brake_air_pressure: float = 0.0
    brake_air_pressure_warning: int = 0
    brake_air_pressure_emergency: int = 0
    brake_temperature: float = 0.0
    fuel: float = 0.0
    fuel_warning: int = 0
    fuel_average_consumption: float = 0.0
    fuel_range: float = 0.0
    adblue: float = 0.0
    adblue_warning: int = 0
    adblue_average_consumption: float = 0.0
    oil_pressure: float = 0.0
    oil_pressure_warning: int = 0
    oil_temperature: float = 0.0
    water_temperature: float = 0.0
    water_temperature_warning: int = 0
    battery_voltage: float = 0.0
    battery_voltage_warning: int = 0
    electric_enabled: int = 0
    engine_enabled: int = 0
    lblinker: int = 0
    rblinker: int = 0
    light_lblinker: int = 0
    light_rblinker: int = 0
    light_parking: int = 0
    light_low_beam: int = 0
    light_high_beam: int = 0
    light_aux_front: int = 0
    light_aux_roof: int = 0
    light_beacon: int = 0
    light_brake: int = 0
    light_reverse: int = 0
    wipers: int = 0
    dashboard_backlight: float = 0.0
    wear_engine: float = 0.0
    wear_transmission: float = 0.0
    wear_cabin: float = 0.0
    wear_chassis: float = 0.0
    wear_wheels: float = 0.0
    odometer: float = 0.0
    navigation_distance: float = 0.0
    navigation_time: float = 0.0
    navigation_speed_limit: float = 0.0
    wheel_susp_deflection = [0.0] * TELE_TRUCK_WHEEL_COUNT
    wheel_on_ground = [0] * TELE_TRUCK_WHEEL_COUNT
    wheel_substance = [0] * TELE_TRUCK_WHEEL_COUNT
    wheel_velocity = [0.0] * TELE_TRUCK_WHEEL_COUNT
    wheel_steering = [0.0] * TELE_TRUCK_WHEEL_COUNT
    wheel_rotation = [0.0] * TELE_TRUCK_WHEEL_COUNT
    wheel_lift = [0.0] * TELE_TRUCK_WHEEL_COUNT
    wheel_lift_offset = [0.0] * TELE_TRUCK_WHEEL_COUNT

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        data_stream = DataStream(data, offset)
        truck = Truck()
        truck.world_placement = data_stream.getPlacement()
        truck.local_linear_velocity = data_stream.getVector()
        truck.local_angular_velocity = data_stream.getVector()
        truck.local_linear_acceleration = data_stream.getVector()
        truck.local_angular_acceleration = data_stream.getVector()
        truck.cabin_offset = data_stream.getPlacement()
        truck.cabin_angular_velocity = data_stream.getVector()
        truck.cabin_angular_acceleration = data_stream.getVector()
        truck.head_offset = data_stream.getPlacement()
        truck.speed = data_stream.getFloat()
        truck.engine_rpm = data_stream.getFloat()
        truck.engine_gear = data_stream.getInt32()
        truck.displayed_gear = data_stream.getInt32()
        truck.input_steering = data_stream.getFloat()
        truck.input_throttle = data_stream.getFloat()
        truck.input_brake = data_stream.getFloat()
        truck.input_clutch = data_stream.getFloat()
        truck.effective_steering = data_stream.getFloat()
        truck.effective_throttle = data_stream.getFloat()
        truck.effective_brake = data_stream.getFloat()
        truck.effective_clutch = data_stream.getFloat()
        truck.cruise_control = data_stream.getFloat()
        truck.hshifter_slot = data_stream.getUInt32()
        truck.parking_brake = data_stream.getUInt8()
        truck.motor_brake = data_stream.getUInt8()
        truck.retarder_level = data_stream.getUInt32()
        truck.brake_air_pressure = data_stream.getFloat()
        truck.brake_air_pressure_warning = data_stream.getUInt8()
        truck.brake_air_pressure_emergency = data_stream.getUInt8()
        truck.brake_temperature = data_stream.getFloat()
        truck.fuel = data_stream.getFloat()
        truck.fuel_warning = data_stream.getUInt8()
        truck.fuel_average_consumption = data_stream.getFloat()
        truck.fuel_range = data_stream.getFloat()
        truck.adblue = data_stream.getFloat()
        truck.adblue_warning = data_stream.getUInt8()
        truck.adblue_average_consumption = data_stream.getFloat()
        truck.oil_pressure = data_stream.getFloat()
        truck.oil_pressure_warning = data_stream.getUInt8()
        truck.oil_temperature = data_stream.getFloat()
        truck.water_temperature = data_stream.getFloat()
        truck.water_temperature_warning = data_stream.getUInt8()
        truck.battery_voltage = data_stream.getFloat()
        truck.battery_voltage_warning = data_stream.getUInt8()
        truck.electric_enabled = data_stream.getUInt8()
        truck.engine_enabled = data_stream.getUInt8()
        truck.lblinker = data_stream.getUInt8()
        truck.rblinker = data_stream.getUInt8()
        truck.light_lblinker = data_stream.getUInt8()
        truck.light_rblinker = data_stream.getUInt8()
        truck.light_parking = data_stream.getUInt8()
        truck.light_low_beam = data_stream.getUInt8()
        truck.light_high_beam = data_stream.getUInt8()
        truck.light_aux_front = data_stream.getUInt32()
        truck.light_aux_roof = data_stream.getUInt32()
        truck.light_beacon = data_stream.getUInt8()
        truck.light_brake = data_stream.getUInt8()
        truck.light_reverse = data_stream.getUInt8()
        truck.wipers = data_stream.getUInt8()
        truck.dashboard_backlight = data_stream.getFloat()
        truck.wear_engine = data_stream.getFloat()
        truck.wear_transmission = data_stream.getFloat()
        truck.wear_cabin = data_stream.getFloat()
        truck.wear_chassis = data_stream.getFloat()
        truck.wear_wheels = data_stream.getFloat()
        truck.odometer = data_stream.getFloat()
        truck.navigation_distance = data_stream.getFloat()
        truck.navigation_time = data_stream.getFloat()
        truck.navigation_speed_limit = data_stream.getFloat()
        truck.wheel_susp_deflection = [data_stream.getFloat() for _ in range(TELE_TRUCK_WHEEL_COUNT)]
        truck.wheel_on_ground = [data_stream.getUInt8() for _ in range(TELE_TRUCK_WHEEL_COUNT)]
        truck.wheel_substance = [data_stream.getUInt32() for _ in range(TELE_TRUCK_WHEEL_COUNT)]
        truck.wheel_velocity = [data_stream.getFloat() for _ in range(TELE_TRUCK_WHEEL_COUNT)]
        truck.wheel_steering = [data_stream.getFloat() for _ in range(TELE_TRUCK_WHEEL_COUNT)]
        truck.wheel_rotation = [data_stream.getFloat() for _ in range(TELE_TRUCK_WHEEL_COUNT)]
        truck.wheel_lift = [data_stream.getFloat() for _ in range(TELE_TRUCK_WHEEL_COUNT)]
        truck.wheel_lift_offset = [data_stream.getFloat() for _ in range(TELE_TRUCK_WHEEL_COUNT)]
        return truck

@dataclass
class Trailer:
    connected: int = 0
    world_placement = Placement()
    local_linear_velocity = Vector()
    local_angular_velocity = Vector()
    local_linear_acceleration = Vector()
    local_angular_acceleration = Vector()
    wear_chassis: float = 0.0
    wheel_susp_deflection = [0.0] * TELE_TRAILER_WHEEL_COUNT
    wheel_on_ground = [0] * TELE_TRAILER_WHEEL_COUNT
    wheel_substance = [0] * TELE_TRAILER_WHEEL_COUNT
    wheel_velocity = [0.0] * TELE_TRAILER_WHEEL_COUNT
    wheel_steering = [0.0] * TELE_TRAILER_WHEEL_COUNT
    wheel_rotation = [0.0] * TELE_TRAILER_WHEEL_COUNT

    @staticmethod
    def unpack(data: bytearray, offset = 0):  
        data_stream = DataStream(data, offset)
        trailer = Trailer()
        trailer.connected = data_stream.getUInt8()
        trailer.world_placement = data_stream.getPlacement()
        trailer.local_linear_velocity = data_stream.getVector()
        trailer.local_angular_velocity = data_stream.getVector()
        trailer.local_linear_acceleration = data_stream.getVector()
        trailer.local_angular_acceleration = data_stream.getVector()
        trailer.wear_chassis = data_stream.getFloat()
        trailer.wheel_susp_deflection = [data_stream.getFloat() for _ in range(TELE_TRAILER_WHEEL_COUNT)]
        trailer.wheel_on_ground = [data_stream.getUInt8() for _ in range(TELE_TRAILER_WHEEL_COUNT)]
        trailer.wheel_substance = [data_stream.getUInt32() for _ in range(TELE_TRAILER_WHEEL_COUNT)]
        trailer.wheel_velocity = [data_stream.getFloat() for _ in range(TELE_TRAILER_WHEEL_COUNT)]
        trailer.wheel_steering = [data_stream.getFloat() for _ in range(TELE_TRAILER_WHEEL_COUNT)]
        trailer.wheel_rotation = [data_stream.getFloat() for _ in range(TELE_TRAILER_WHEEL_COUNT)]
        return trailer  

@dataclass
class ConfigTruck:
    brand_id: str = ""
    brand: str = ""
    id: str = ""
    name: str = ""
    fuel_capacity: float = 0.0
    fuel_warning_factor: float = 0.0
    adblue_capacity: float = 0.0
    adblue_warning_factor: float = 0.0
    air_pressure_warning: float = 0.0
    air_pressure_emergency: float = 0.0
    oil_pressure_warning: float = 0.0
    water_temperature_warning: float = 0.0
    battery_voltage_warning: float = 0.0
    rpm_limit: float = 0.0
    forward_gear_count: int = 0
    reverse_gear_count: int = 0
    retarder_step_count: int = 0
    cabin_position = Vector()
    head_position = Vector()
    hook_position = Vector()
    license_plate: str = ""
    license_plate_country: str = ""
    license_plate_country_id: str = ""
    wheel_count: int = 0
    wheel_position = [Vector()] * TELE_TRUCK_WHEEL_COUNT

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        data_stream = DataStream(data, offset)
        config_truck = ConfigTruck()
        config_truck.brand_id = data_stream.getString(TELE_STR_SIZE)
        config_truck.brand = data_stream.getString(TELE_STR_SIZE)
        config_truck.id = data_stream.getString(TELE_STR_SIZE)
        config_truck.name = data_stream.getString(TELE_STR_SIZE)
        config_truck.fuel_capacity = data_stream.getFloat()
        config_truck.fuel_warning_factor = data_stream.getFloat()
        config_truck.adblue_capacity = data_stream.getFloat()
        config_truck.adblue_warning_factor = data_stream.getFloat()
        config_truck.air_pressure_warning = data_stream.getFloat()
        config_truck.air_pressure_emergency = data_stream.getFloat()
        config_truck.oil_pressure_warning = data_stream.getFloat()
        config_truck.water_temperature_warning = data_stream.getFloat()
        config_truck.battery_voltage_warning = data_stream.getFloat()
        config_truck.rpm_limit = data_stream.getFloat()
        config_truck.forward_gear_count = data_stream.getUInt32()
        config_truck.reverse_gear_count = data_stream.getUInt32()
        config_truck.retarder_step_count = data_stream.getUInt32()
        config_truck.cabin_position = data_stream.getVector()
        config_truck.head_position = data_stream.getVector()
        config_truck.hook_position = data_stream.getVector()
        config_truck.license_plate = data_stream.getString(TELE_STR_SIZE)
        config_truck.license_plate_country = data_stream.getString(TELE_STR_SIZE)
        config_truck.license_plate_country_id = data_stream.getString(TELE_STR_SIZE)
        config_truck.wheel_count = data_stream.getUInt32()
        config_truck.wheel_position = [data_stream.getVector() for _ in range(TELE_TRUCK_WHEEL_COUNT)]
        return config_truck

@dataclass
class ConfigTrailer:
    index: int = 0
    id: str = ""
    cargo_accessory_id: str = ""
    hook_position = Vector()
    brand_id: str = ""
    brand: str = ""
    name: str = ""
    chain_type: str = ""
    body_type: str = ""
    license_plate: str = ""
    license_plate_country: str = ""
    license_plate_country_id: str = ""
    wheel_count: int = 0
    wheel_position = [Vector()] * TELE_TRAILER_WHEEL_COUNT

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        data_stream = DataStream(data, offset)
        config_trailer = ConfigTrailer()
        config_trailer.index = data_stream.getUInt8()
        config_trailer.id = data_stream.getString(TELE_STR_SIZE)
        config_trailer.cargo_accessory_id = data_stream.getString(TELE_STR_SIZE)
        config_trailer.hook_position = data_stream.getVector()
        config_trailer.brand_id = data_stream.getString(TELE_STR_SIZE)
        config_trailer.brand = data_stream.getString(TELE_STR_SIZE)
        config_trailer.name = data_stream.getString(TELE_STR_SIZE)
        config_trailer.chain_type = data_stream.getString(TELE_STR_SIZE)
        config_trailer.body_type = data_stream.getString(TELE_STR_SIZE)
        config_trailer.license_plate = data_stream.getString(TELE_STR_SIZE)
        config_trailer.license_plate_country = data_stream.getString(TELE_STR_SIZE)
        config_trailer.license_plate_country_id = data_stream.getString(TELE_STR_SIZE)
        config_trailer.wheel_count = data_stream.getUInt32()
        config_trailer.wheel_position = [data_stream.getVector() for _ in range(TELE_TRAILER_WHEEL_COUNT)]
        return config_trailer

@dataclass
class ConfigJob:
    cargo_id: str = ""
    cargo: str = ""
    cargo_mass: float = 0.0
    destination_city_id: str = ""
    destination_city: str = ""
    source_city_id: str = ""
    source_city: str = ""
    destination_company_id: str = ""
    destination_company: str = ""
    source_company_id: str = ""
    source_company: str = ""
    income: int = 0
    delivery_time: int = 0
    is_cargo_loaded: int = 0
    job_market: str = ""
    special_job: int = 0
    planned_distance_km: int = 0

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        data_stream = DataStream(data, offset)
        config_job = ConfigJob()
        config_job.cargo_id = data_stream.getString(TELE_STR_SIZE)
        config_job.cargo = data_stream.getString(TELE_STR_SIZE)
        config_job.cargo_mass = data_stream.getFloat()
        config_job.destination_city_id = data_stream.getString(TELE_STR_SIZE)   
        config_job.destination_city = data_stream.getString(TELE_STR_SIZE)      
        config_job.source_city_id = data_stream.getString(TELE_STR_SIZE)        
        config_job.source_city = data_stream.getString(TELE_STR_SIZE)
        config_job.destination_company_id = data_stream.getString(TELE_STR_SIZE)
        config_job.destination_company = data_stream.getString(TELE_STR_SIZE)   
        config_job.source_company_id = data_stream.getString(TELE_STR_SIZE)     
        config_job.source_company = data_stream.getString(TELE_STR_SIZE)        
        config_job.income = data_stream.getUInt64()
        config_job.delivery_time = data_stream.getUInt32()
        config_job.is_cargo_loaded = data_stream.getUInt8()
        config_job.job_market = data_stream.getString(TELE_STR_SIZE)
        config_job.special_job = data_stream.getUInt8()
        config_job.planned_distance_km = data_stream.getUInt32()
        return config_job

class Client:
    def __init__(self):
        self.__sock = None
        self.__address = None
        self.__heartbeat_last_time = 0
        self.common = Common()
        self.truck = Truck()
        self.trailer = Trailer()

        self.config_truck = ConfigTruck()
        self.config_trailer = [ConfigTrailer() for i in range(TELE_TRAILER_COUNT)]
        self.config_job = ConfigJob

    def connect(self, ip: str, port: int):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.settimeout(0.1)
        self.__address = (ip, port)

    def update(self):
        time_now = time.time()
        if(time_now - self.__heartbeat_last_time > 1.0):
            heartbeat = bytearray([TELE_PACKET_HEARTBEAT, 0xFF])
            self.__sock.sendto(heartbeat, self.__address)

        try:
            data = self.__sock.recv(4096)
        except socket.timeout:
            return

        packet_type = int(data[0])

        if(packet_type == TELE_PACKET_COMMON):
            self.common = Common.unpack(data, offset=1)
        elif(packet_type == TELE_PACKET_TRUCK):
            self.truck = Truck.unpack(data, offset=1)
        elif(packet_type == TELE_PACKET_TRAILER):
            self.trailer = Trailer.unpack(data, offset=1)
        elif(packet_type == TELE_PACKET_CONFIG_TRUCK):
            self.config_truck = ConfigTruck.unpack(data, offset=1)
        elif(packet_type == TELE_PACKET_CONFIG_TRAILER):
            self.config_trailer = ConfigTrailer.unpack(data, offset=1)
        elif(packet_type == TELE_PACKET_CONFIG_JOB):
            self.config_job = ConfigJob.unpack(data, offset=1)
        else:
            print("Unknown packet type: %s" % packet_type)

    def close(self):
        self.__sock.close()
