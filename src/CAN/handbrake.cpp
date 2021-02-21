#include "e90canbus.h"
#include "globals.h"

const uint16_t CAN_ID = 0x34F;
uint8_t handbrake_frame[2] = {0xFE, 0xFF};

void canSendHandbrake(){
  if(s_handbrake){
    handbrake_frame[0] = 0xFE;
  }else{
    handbrake_frame[0] = 0xFD;
  }
  CAN.sendMsgBuf(CAN_ID, 0, 2, handbrake_frame);
}
