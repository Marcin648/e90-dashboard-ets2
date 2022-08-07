#pragma once

#include <mcp2515.h>

/*
    Project configuration file
*/

// General
#define STATUS_LED_PIN LED_BUILTIN

// Serial
#define SERIAL_BOUD_RATE 115200

// CAN
#define MCP_CS_PIN 9
#define MCP_CLOCK MCP_8MHZ
#define CAN_BAUD_RATE CAN_100KBPS
