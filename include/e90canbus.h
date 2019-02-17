#pragma once

#include <Arduino.h>

#include <stdio.h>
#include <stdint.h>
#include <mcp_can.h>
#include <SPI.h>

extern MCP_CAN CAN;

//Main can data loop
void canSend();
