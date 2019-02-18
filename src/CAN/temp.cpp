#include "../include/e90canbus.h"

uint8_t engine_temp_frame[8] = {0x8B, 0xFF, 0x63, 0xCD, 0x5D, 0x37, 0xCD, 0xA8};

const uint16_t CAN_ID = 0x1D0;

void canSendEngineTemp(){
  engine_temp_frame[0] = s_engine_temp + 48;
  engine_temp_frame[2]++;
  CAN.sendMsgBuf(CAN_ID, 0, 8, engine_temp_frame);
}
