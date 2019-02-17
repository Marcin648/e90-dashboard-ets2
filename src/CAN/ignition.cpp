#include "../include/e90canbus.h"

uint8_t ignition_frame_on[5] = {0x45, 0x42, 0x69, 0x8f, 0xE2};
uint8_t ignition_frame_off[5] = {0x00, 0x00, 0xC0, 0x0f, 0xE2};

const uint16_t CAN_ID = 0x130;

void canSendIgnitionFrame(){
  if(s_ignition){
    CAN.sendMsgBuf(CAN_ID, 0, 5, ignition_frame_on);
    ignition_frame_on[4]++;
  }else{
    CAN.sendMsgBuf(CAN_ID, 0, 5, ignition_frame_off);
    ignition_frame_off[4]++;
  }
}
