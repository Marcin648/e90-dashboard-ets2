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
//Constant
extern const uint8_t DTIME_MULTIPLE;


/*
  Functions
*/

void canSendIgnitionFrame();
void canSendSteeringWheel();
void canSendLights();
void canSendFuel();
void canSendIndicator();
void canSendAbs();
void canSendHandbrake();
void canSendRPM();
void canSendSpeed();
void canSendTime();
void canSendEngineTemp();

void canSendAbsCounter();
void canSendAirbagCounter();

//Main can data loop
void canSend();
