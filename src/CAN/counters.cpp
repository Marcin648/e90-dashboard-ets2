#include "e90canbus.h"
#include "globals.h"

const uint16_t ABS_COUNTER_CAN_ID = 0x0C0;
uint8_t abs_counter_frame[2] = {0xF0, 0xFF};

void canSendAbsCounter(){
  CAN.sendMsgBuf(ABS_COUNTER_CAN_ID, 0, 2, abs_counter_frame);
  abs_counter_frame[0] = ((abs_counter_frame[0] + 1) | 0xF0);
}

const uint16_t AIRBAG_COUNTER_CAN_ID = 0x0D7;
uint8_t airbag_counter_frame[2] = {0xC3, 0xFF};

void canSendAirbagCounter(){
  CAN.sendMsgBuf(AIRBAG_COUNTER_CAN_ID, 0, 2, airbag_counter_frame);
  airbag_counter_frame[0]++;
}
