#include <Arduino.h>
#include <SPI.h>
#include <mcp2515.h>

#include "Configuration.hpp"
#include "StatusLed.hpp"
#include "CanFrames.hpp"

MCP2515 mcp(MCP_CS_PIN);
StatusLed status_led(STATUS_LED_PIN);

CanFrameAbs frame_abs(&mcp);
CanFrameAbsCounter frame_abs_counter(&mcp);
CanFrameAirbagCounter frame_airbag_counter(&mcp);
CanFrameIgnation frame_ignation(&mcp);

void setup(){
    MCP2515::ERROR mcp_error;
    Serial.begin(SERIAL_BOUD_RATE);

    mcp_error = mcp.reset();
    if(mcp_error != MCP2515::ERROR_OK) status_led.fatal_loop(5);

    mcp_error = mcp.setBitrate(CAN_BAUD_RATE, MCP_CLOCK);
    if(mcp_error != MCP2515::ERROR_OK) status_led.fatal_loop(5);

    mcp_error = mcp.setNormalMode();
    if(mcp_error != MCP2515::ERROR_OK) status_led.fatal_loop(5);
}

void loop(){
    frame_abs.update();
    frame_abs_counter.update();
    frame_airbag_counter.update();
    frame_ignation.update();
}