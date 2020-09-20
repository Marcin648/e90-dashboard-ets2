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

@dataclass
class Vector:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @staticmethod
    def size():
        return struct.calcsize("<Bfff")

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        return Vector(struct.unpack_from("<Bfff", data, offset=offset))

@dataclass
class Euler:
    heading: float = 0.0
    pitch: float = 0.0
    roll: float = 0.0

    @staticmethod
    def size():
        return struct.calcsize("<Bfff")

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        return Euler(struct.unpack_from("<Bfff", data, offset=offset))

@dataclass
class Placement:
    position: Vector = Vector()
    orientation: Euler = Euler()

    @staticmethod
    def size():
        return Vector.size() + Euler.size()

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        placement = Placement()
        placement.position = Vector.unpack(data, offset)
        placement.orientation = Euler.unpack(data, offset = offset + Vector.size())
        return placement

@dataclass
class Common:
    game_paused: bool = False
    local_scale: float = 0.0
    game_time: int = 0
    next_rest_stop: int = 0

    @staticmethod
    def size():
        return struct.calcsize("<BfIi")

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        return Common(*struct.unpack_from("<BfIi", data, offset=offset))


        
@dataclass
class Truck():
    __world_placement_x: float = 0.0
    __world_placement_y: float = 0.0
    __world_placement_z: float = 0.0
    __world_placement_heading: float = 0.0
    __world_placement_pitch: float = 0.0
    __world_placement_roll: float = 0.0
    __local_linear_velocity_x: float = 0.0
    __local_linear_velocity_y: float = 0.0
    __local_linear_velocity_z: float = 0.0
    __local_angular_velocity_x: float = 0.0
    __local_angular_velocity_y: float = 0.0
    __local_angular_velocity_z: float = 0.0
    __local_linear_acceleration_x: float = 0.0
    __local_linear_acceleration_y: float = 0.0
    __local_linear_acceleration_z: float = 0.0
    __local_angular_acceleration_x: float = 0.0
    __local_angular_acceleration_y: float = 0.0
    __local_angular_acceleration_z: float = 0.0
    __cabin_offset_x: float = 0.0
    __cabin_offset_y: float = 0.0
    __cabin_offset_z: float = 0.0
    __cabin_offset_heading: float = 0.0
    __cabin_offset_pitch: float = 0.0
    __cabin_offset_roll: float = 0.0
    __cabin_angular_velocity_x: float = 0.0
    __cabin_angular_velocity_y: float = 0.0
    __cabin_angular_velocity_z: float = 0.0
    __cabin_angular_acceleration_x: float = 0.0
    __cabin_angular_acceleration_y: float = 0.0
    __cabin_angular_acceleration_z: float = 0.0
    __head_offset_x: float = 0.0
    __head_offset_y: float = 0.0
    __head_offset_z: float = 0.0
    __head_offset_heading: float = 0.0
    __head_offset_pitch: float = 0.0
    __head_offset_roll: float = 0.0
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

    world_placement = Placement()
    local_linear_velocity = Vector()
    local_angular_velocity = Vector()
    local_linear_acceleration = Vector()
    local_angular_acceleration = Vector()
    cabin_offset = Placement()
    cabin_angular_velocity = Vector()
    cabin_angular_acceleration = Vector()
    head_offset = Placement()

    @staticmethod
    def size():
        size = 0
        size += struct.calcsize("<38f2i9fI2BIf2B2fB3fB2fB2fBf10B2I4B10f")
        size += struct.calcsize("<fBI5f") * TELE_TRUCK_WHEEL_COUNT
        return size

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        truck = Truck(*struct.unpack_from("<38f2i9fI2BIf2B2fB3fB2fB2fBf10B2I4B10f", data, offset=offset))
        offset += struct.calcsize("<38f2i9fI2BIf2B2fB3fB2fB2fBf10B2I4B10f")

        truck.wheel_susp_deflection = struct.unpack_from("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f")

        truck.wheel_on_ground = struct.unpack_from("<" + str(TELE_TRUCK_WHEEL_COUNT) + "B", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRUCK_WHEEL_COUNT) + "B")

        truck.wheel_substance = struct.unpack_from("<" + str(TELE_TRUCK_WHEEL_COUNT) + "I", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRUCK_WHEEL_COUNT) + "I")

        truck.wheel_velocity = struct.unpack_from("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f")

        truck.wheel_steering = struct.unpack_from("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f")

        truck.wheel_rotation = struct.unpack_from("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f")

        truck.wheel_lift = struct.unpack_from("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f")

        truck.wheel_lift_offset = struct.unpack_from("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRUCK_WHEEL_COUNT) + "f")

        truck.world_placement = Placement(
            Vector(truck.__world_placement_x, truck.__world_placement_y, truck.__world_placement_z),
            Euler(truck.__world_placement_heading, truck.__world_placement_pitch, truck.__world_placement_roll)
        )
        truck.local_linear_velocity = Vector(
            truck.__local_linear_velocity_x, truck.__local_linear_velocity_y, truck.__local_linear_velocity_z
        )
        truck.local_angular_velocity = Vector(
            truck.__local_angular_velocity_x, truck.__local_angular_velocity_y, truck.__local_angular_velocity_z
        )
        truck.local_linear_acceleration = Vector(
            truck.__local_linear_acceleration_x, truck.__local_linear_acceleration_y, truck.__local_linear_acceleration_z
        )
        truck.local_angular_acceleration = Vector(
            truck.__local_angular_acceleration_x, truck.__local_angular_acceleration_y, truck.__local_angular_acceleration_z
        )
        truck.cabin_offset = Placement(
            Vector(truck.__cabin_offset_x, truck.__cabin_offset_y, truck.__cabin_offset_z),
            Euler(truck.__cabin_offset_heading, truck.__cabin_offset_pitch, truck.__cabin_offset_roll)
        )
        truck.cabin_angular_velocity = Vector(
            truck.__cabin_angular_velocity_x, truck.__cabin_angular_velocity_y, truck.__cabin_angular_velocity_z
        )
        truck.cabin_angular_acceleration = Vector(
            truck.__cabin_angular_acceleration_x, truck.__cabin_angular_acceleration_y, truck.__cabin_angular_acceleration_z
        )
        truck.head_offset = Placement(
            Vector(truck.__head_offset_x, truck.__head_offset_y, truck.__head_offset_z),
            Euler(truck.__head_offset_heading, truck.__head_offset_pitch, truck.__head_offset_roll)
        )

        return truck

@dataclass
class Trailer:
    connected: int = 0
    __world_placement_x: float = 0.0
    __world_placement_y: float = 0.0
    __world_placement_z: float = 0.0
    __world_placement_heading: float = 0.0
    __world_placement_pitch: float = 0.0
    __world_placement_roll: float = 0.0
    __local_linear_velocity_x: float = 0.0
    __local_linear_velocity_y: float = 0.0
    __local_linear_velocity_z: float = 0.0
    __local_angular_velocity_x: float = 0.0
    __local_angular_velocity_y: float = 0.0
    __local_angular_velocity_z: float = 0.0
    __local_linear_acceleration_x: float = 0.0
    __local_linear_acceleration_y: float = 0.0
    __local_linear_acceleration_z: float = 0.0
    __local_angular_acceleration_x: float = 0.0
    __local_angular_acceleration_y: float = 0.0
    __local_angular_acceleration_z: float = 0.0
    wear_chassis: float = 0.0
    wheel_susp_deflection = [0.0] * TELE_TRAILER_WHEEL_COUNT
    wheel_on_ground = [0] * TELE_TRAILER_WHEEL_COUNT
    wheel_substance = [0] * TELE_TRAILER_WHEEL_COUNT
    wheel_velocity = [0.0] * TELE_TRAILER_WHEEL_COUNT
    wheel_steering = [0.0] * TELE_TRAILER_WHEEL_COUNT
    wheel_rotation = [0.0] * TELE_TRAILER_WHEEL_COUNT

    world_placement = Placement()
    local_linear_velocity = Vector()
    local_angular_velocity = Vector()
    local_linear_acceleration = Vector()
    local_angular_acceleration = Vector()

    @staticmethod
    def size():
        size = 0
        size += struct.calcsize("<B19f")
        size += struct.calcsize("<fBI3f") * TELE_TRAILER_WHEEL_COUNT
        return size

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        trailer = Trailer(*struct.unpack_from("<B19f", data, offset=offset))
        offset += struct.calcsize("<B19f")

        trailer.wheel_susp_deflection = struct.unpack_from("<" + str(TELE_TRAILER_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRAILER_WHEEL_COUNT) + "f")

        trailer.wheel_on_ground = struct.unpack_from("<" + str(TELE_TRAILER_WHEEL_COUNT) + "B", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRAILER_WHEEL_COUNT) + "B")

        trailer.wheel_substance = struct.unpack_from("<" + str(TELE_TRAILER_WHEEL_COUNT) + "I", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRAILER_WHEEL_COUNT) + "I")

        trailer.wheel_velocity = struct.unpack_from("<" + str(TELE_TRAILER_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRAILER_WHEEL_COUNT) + "f")

        trailer.wheel_steering = struct.unpack_from("<" + str(TELE_TRAILER_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRAILER_WHEEL_COUNT) + "f")

        trailer.wheel_rotation = struct.unpack_from("<" + str(TELE_TRAILER_WHEEL_COUNT) + "f", data, offset=offset)
        offset += struct.calcsize("<" + str(TELE_TRAILER_WHEEL_COUNT) + "f")

        trailer.world_placement = Placement(
            Vector(trailer.__world_placement_x, trailer.__world_placement_y, trailer.__world_placement_z),
            Euler(trailer.__world_placement_heading, trailer.__world_placement_pitch, trailer.__world_placement_roll)
        )
        trailer.local_linear_velocity = Vector(
            trailer.__local_linear_velocity_x, trailer.__local_linear_velocity_y, trailer.__local_linear_velocity_z
        )
        trailer.local_angular_velocity = Vector(
            trailer.__local_angular_velocity_x, trailer.__local_angular_velocity_y, trailer.__local_angular_velocity_z
        )
        trailer.local_linear_acceleration = Vector(
            trailer.__local_linear_acceleration_x, trailer.__local_linear_acceleration_y, trailer.__local_linear_acceleration_z
        )
        trailer.local_angular_acceleration = Vector(
            trailer.__local_angular_acceleration_x, trailer.__local_angular_acceleration_y, trailer.__local_angular_acceleration_z
        )

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
    def size():
        #TODO
        pass

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        #TODO
        pass

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
    def size():
        #TODO
        pass

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        #TODO
        pass

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
    def size():
        #TODO
        pass

    @staticmethod
    def unpack(data: bytearray, offset = 0):
        #TODO
        pass

class Client:
    def __init__(self):
        self.__sock = socket.socket()
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
        #elif(packet_type == TELE_PACKET_CONFIG_TRUCK):
            #self.config_truck = ConfigTruck.unpack(data, offset=1)
        else:
            pass
            #print(packet_type)


    def close(self):
        self.__sock.close()

if __name__ == "__main__":
    a = Client()
    a.connect("127.0.0.1", 23444)
    for _ in range(1000):
        a.update()
    a.close()
    pass