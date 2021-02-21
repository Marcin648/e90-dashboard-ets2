#include "globals.h"
#include "e90types.h"

//States
bool s_ignition = false;

bool s_light_parking = false;
bool s_light_dip = false;
bool s_light_main = false;
bool s_light_fog = false;
bool s_handbrake = false;
uint8_t s_light_indicator = I_OFF;
uint16_t s_speed = 0;
uint16_t s_rpm = 0;
uint16_t s_fuel = 0; // 1000 - max;
uint8_t s_engine_temp = 91;

uint8_t s_time_hour = 0;
uint8_t s_time_minute = 0;
uint8_t s_time_sec = 0;
uint8_t s_time_day = 1;
uint8_t s_time_month = 1;
uint16_t s_time_year = 2019;