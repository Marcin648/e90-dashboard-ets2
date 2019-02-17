#include "e90canbus.h"


uint32_t lastTime = 0;
uint16_t canCounter = 0;

void canSend(){
  uint32_t courentTime = millis();
  if(courentTime - lastTime > 100){
    //100 ms interval
    printf("100ms\n");
    if(canCounter % 2 == 0){ //200 ms interval
      printf("200ms\n");;
    }

    if(canCounter % 5 == 0){ //500 ms interval
      printf("500ms\n");;
    }

    if(canCounter % 10 == 0){ //1000 ms interval
      printf("1000ms\n");;
    }

    canCounter++;
    lastTime = courentTime;
  }
}
