#pragma once

#include <Arduino.h>

#include <stdio.h>
#include <stdint.h>
#include <mcp_can.h>
#include <SPI.h>

/*
  Globals
*/

//States
extern bool s_ignition;

extern bool s_light_dip;
extern bool s_light_main;
extern bool s_light_fog;

extern float s_fuel;

//CAN object
extern MCP_CAN CAN;

/*
  Functions
*/

void canSendIgnitionFrame();

//Main can data loop
void canSend();
