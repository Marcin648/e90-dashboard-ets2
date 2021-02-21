#include "e90canbus.h"

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
    canSendRPM();
    canSendSpeed();

    if(canCounter % 2 == 0){ //200 ms interval
      canSendLights();
      canSendAbs();
      canSendEngineTemp();

      canSendAbsCounter();
      canSendAirbagCounter();
    }

    if(canCounter % 5 == 0){ //500 ms interval
      canSendHandbrake();
      canSendFuel();
    }

    if(canCounter % 6 == 0){ //600 ms interval
      canSendIndicator();
    }

    if(canCounter % 10 == 0){ //1000 ms interval
      canSendTime();
    }

    canCounter++;
    lastTime = courentTime;
  }
}
