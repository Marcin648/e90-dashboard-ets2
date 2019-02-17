#include "e90canbus.h"

/*
  Globals
*/

//States
bool s_ignition = false;

bool s_light_parking = false;
bool s_light_dip = false;
bool s_light_main = false;
bool s_light_fog = false;

uint8_t s_light_indicator = I_OFF;

uint16_t s_fuel = 0; // 1000 - max;

//Timing
uint32_t lastTime = 0;
uint16_t canCounter = 0;

/*
  Functions
*/

void canSend(){
  uint32_t courentTime = millis();
  if(courentTime - lastTime > 100){
    //100 ms interval
    canSendIgnitionFrame();

    if(canCounter % 2 == 0){ //200 ms interval
      canSendLights();
    }

    if(canCounter % 5 == 0){ //500 ms interval
      canSendFuel();
    }

    if(canCounter % 10 == 0){ //1000 ms interval
      canSendIndicator();
    }

    canCounter++;
    lastTime = courentTime;
  }
}
