#pragma once

/*
  STATE ENUMS
*/

/*
  CAN ENUMS
*/
typedef enum{
  L_BRAKE = 0b10000000,
  L_FOG = 0b01000000,
  L_BACKLIGHT = 0b00000100,
  L_MAIN = 0b00000010,
  L_DIP = 0b00100000,
} LIGHTS;
