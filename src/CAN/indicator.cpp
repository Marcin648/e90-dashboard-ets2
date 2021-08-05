#include "e90canbus.h"
#include "globals.h"

uint8_t indicator_frame[2] = {0xB1, 0xF2};

const uint16_t CAN_ID = 0x1F6;

uint8_t last_indicator = I_OFF; // off;
unsigned long last_indicator_time = 0;
const unsigned long INDICATOR_OFF_DELAY = 500;

void canSendIndicator(){
  /*
  80 - off

  90 - left constant
  a0 - right constant
  b0 - hazzard constant

  91 - left normal blink
  a1 - right normal blink
  b1 - hazzard normal blink

  92 - left fast blink
  a2 - right fast blink
  b2 - hazzard fast blink
  */

  uint8_t light_indicator = last_indicator;
  if(s_light_indicator == I_OFF){
    unsigned long off_delta_time = millis() - last_indicator_time;
    if(off_delta_time > INDICATOR_OFF_DELAY){
      light_indicator = s_light_indicator;
    }
  }else{
    light_indicator = s_light_indicator;
    last_indicator_time = millis();
  }

  if(light_indicator != I_OFF){
    switch (light_indicator) {
      case I_LEFT:
        indicator_frame[0] = 0x91;
        break;
      case I_RIGHT:
        indicator_frame[0] = 0xA1;
        break;
      case I_HAZZARD:
        indicator_frame[0] = 0xB1;
        break;
    }

    if(last_indicator == light_indicator){
      indicator_frame[1] = 0xF0;
    }else{
      indicator_frame[1] = 0xF0;
    }
  }else{
    indicator_frame[0] = 0x82;
    indicator_frame[1] = 0xF0;
  }

  last_indicator = light_indicator;
  CAN.sendMsgBuf(CAN_ID, 0, 2, indicator_frame);
}
