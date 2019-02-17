#include "../include/e90canbus.h"

uint8_t fuel_frame[5] = {0x00, 0x00, 0x00, 0x00, 0x00};

const uint16_t CAN_ID = 0x349;

void canSendFuel(){
  uint16_t level = min(100+(s_fuel*8), 8000);
  fuel_frame[0] = level;
  fuel_frame[1] = (level >> 8);

  fuel_frame[2] = fuel_frame[0];
  fuel_frame[3] = fuel_frame[1];

  CAN.sendMsgBuf(CAN_ID, 0, 5, fuel_frame);
}
