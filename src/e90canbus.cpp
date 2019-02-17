#include "e90canbus.h"

/*
  Globals
*/

//States
bool s_ignition = true;

bool s_light_parking = true;
bool s_light_dip = true;
bool s_light_main = true;
bool s_light_fog = true;
bool s_handbrake = false;
uint8_t s_light_indicator = I_OFF;
uint16_t s_fuel = 590; // 1000 - max;

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
      canSendAbs();

      canSendAbsCounter();
      canSendAirbagCounter();
    }

    if(canCounter % 5 == 0){ //500 ms interval
      canSendFuel();
      canSendHandbrake();
    }

    if(canCounter % 10 == 0){ //1000 ms interval
      canSendIndicator();
    }

    canCounter++;
    lastTime = courentTime;
  }
}
