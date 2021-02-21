#include "e90canbus.h"
#include "globals.h"

uint8_t indicator_frame[2] = {0xB1, 0xF2};

const uint16_t CAN_ID = 0x1F6;

uint8_t lastIndicator = I_OFF; // off;
void canSendIndicator(){
  /*
  80 - off
  91 - left
  a1 - right
  b1 - hazzard
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
