#include "serial.h"

/*
  Data packet:
  uint8_t - Magic 'Q'
  uint8_t - Ignition
  uint8_t - Parking lights
  uint8_t - Dipped lights
  uint8_t - Main lights
  uint8_t - Fog lights
  uint8_t - Blinkers
            0 - Off
            1 - Left
            2 - Right
            3 - Hazzard
  uint8_t - Handbrake
  uint16_t - RPM
  uint16_t - Speed
  uint16_t - Fuel

  uint8_t - Hour
  uint8_t - Minute
  uint8_t - Second

  uint8_t - Day
  uint8_t - Month
  uint16_t - Year
*/

struct __attribute__((packed)) SerialPacket{
  uint8_t ignition;
  uint8_t parking_lights;
  uint8_t dipped_lights;
  uint8_t main_lights;
  uint8_t fog_lights;
  uint8_t blinkers;

  uint8_t handbrake;
  uint16_t RPM;
  uint16_t speed;
  uint16_t fuel;

  uint8_t hour;
  uint8_t minute;
  uint8_t second;

  uint8_t day;
  uint8_t month;
  uint16_t year;
};

SerialPacket serialPacket;

void serialReceive(){
  if(Serial.read() != 'Q') return;

  if(Serial.readBytes((uint8_t*)&serialPacket, sizeof(SerialPacket)) == sizeof(SerialPacket)){
    s_ignition = serialPacket.ignition;
    s_light_parking = serialPacket.parking_lights;
    s_light_dip = serialPacket.dipped_lights;
    s_light_main = serialPacket.main_lights;
    s_light_fog = serialPacket.fog_lights;
    s_light_indicator = serialPacket.blinkers;

    s_handbrake = serialPacket.handbrake;
    s_rpm = serialPacket.RPM;
    s_speed = serialPacket.speed;
    s_fuel = serialPacket.fuel;

    s_time_hour = serialPacket.hour;
    s_time_minute = serialPacket.minute;
    s_time_sec = serialPacket.second;

    s_time_day = serialPacket.day;
    s_time_month = serialPacket.month;
    s_time_year = serialPacket.year;
  }
  Serial.write('O');
}
