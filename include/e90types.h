#pragma once

/*
  STATE ENUMS
*/
typedef enum{
  I_OFF = 0,
  I_LEFT = 1,
  I_RIGHT = 2,
  I_HAZZARD = 3,
} INDICATOR;


/*
  CAN ENUMS
*/
typedef enum{
  L_BRAKE = 0b10000000,
  L_FOG = 0b01000000,
  L_BACKLIGHT = 0b00000100,
  L_MAIN = 0b00000010,
  L_DIP = 0b00100000,
} CAN_LIGHTS;
