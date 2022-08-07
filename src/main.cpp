#include <Arduino.h>
#include <SPI.h>
#include <mcp2515.h>

#include "Configuration.hpp"
#include "StatusLed.hpp"

MCP2515 mcp2515(MCP_CS_PIN);
StatusLed status_led(STATUS_LED_PIN);

void setup(){
    MCP2515::ERROR mcp_error;
    Serial.begin(SERIAL_BOUD_RATE);

    mcp_error = mcp2515.reset();
    if(mcp_error != MCP2515::ERROR_OK) status_led.fatal_loop(5);

    mcp_error = mcp2515.setBitrate(CAN_BAUD_RATE, MCP_CLOCK);
    if(mcp_error != MCP2515::ERROR_OK) status_led.fatal_loop(5);

    mcp_error = mcp2515.setNormalMode();
    if(mcp_error != MCP2515::ERROR_OK) status_led.fatal_loop(5);
}

void loop(){
    
}