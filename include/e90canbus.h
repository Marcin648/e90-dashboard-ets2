#pragma once

#include <Arduino.h>

#include <stdio.h>
#include <stdint.h>
#include <mcp_can.h>
#include <SPI.h>

#include "e90types.h"
/*
  Globals
*/

//States
extern bool s_ignition;

extern bool s_light_parking;
extern bool s_light_dip;
extern bool s_light_main;
extern bool s_light_fog;

extern uint8_t s_light_indicator;

extern uint16_t s_fuel;

//CAN object
extern MCP_CAN CAN;

/*
  Functions
*/

void canSendIgnitionFrame();
void canSendLights();
void canSendFuel();
void canSendIndicator();

//Main can data loop
void canSend();
