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

void serialReceive(){
  while(Serial.read() != 'Q'){
    if(!Serial.available()) return;
  }

  s_ignition = Serial.read();

  s_light_parking = Serial.read();
  s_light_dip = Serial.read();
  s_light_main = Serial.read();
  s_light_fog = Serial.read();
  s_light_indicator = Serial.read();

  s_handbrake = Serial.read();

  Serial.readBytes((uint8_t*)&s_rpm, 2);
  Serial.readBytes((uint8_t*)&s_speed, 2);
  Serial.readBytes((uint8_t*)&s_fuel, 2);

  s_time_hour = Serial.read();
  s_time_minute = Serial.read();
  s_time_sec = Serial.read();

  s_time_day = Serial.read();
  s_time_month = Serial.read();
  Serial.readBytes((uint8_t*)&s_time_year, 2);
}
