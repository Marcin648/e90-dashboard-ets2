#pragma once
#include <stdint.h>
#include <mcp2515_can.h>

//States
extern bool s_ignition;
extern bool s_light_parking;
extern bool s_light_dip;
extern bool s_light_main;
extern bool s_light_fog;
extern bool s_handbrake;
extern uint8_t s_light_indicator;
extern uint16_t s_rpm;
extern uint16_t s_speed;
extern uint16_t s_fuel;
extern uint8_t s_engine_temp;

extern uint8_t s_time_hour;
extern uint8_t s_time_minute;
extern uint8_t s_time_sec;
extern uint8_t s_time_day;
extern uint8_t s_time_month;
extern uint16_t s_time_year;

//CAN object
extern mcp2515_can CAN;
