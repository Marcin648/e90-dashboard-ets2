#include "e90canbus.h"
#include "globals.h"

uint8_t indicator_frame[2] = {0xB1, 0xF2};

const uint16_t CAN_ID = 0x1F6;

uint8_t lastIndicator = I_OFF; // off;
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

  if(s_light_indicator != I_OFF){
    switch (s_light_indicator) {
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

    if(lastIndicator == s_light_indicator){
      indicator_frame[1] = 0xF1;
    }else{
      indicator_frame[1] = 0xF2;
    }
  }else{
    indicator_frame[0] = 0x80;
    indicator_frame[1] = 0xF0;
  }

  lastIndicator = s_light_indicator;
  CAN.sendMsgBuf(CAN_ID, 0, 2, indicator_frame);
}
