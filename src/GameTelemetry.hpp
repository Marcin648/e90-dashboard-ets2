#pragma once
#include <stdint.h>
/*
  Data packet:
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

#pragma pack(push, 1)
struct GameTelemetry{
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
#pragma pack(pop)