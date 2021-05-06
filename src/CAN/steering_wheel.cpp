#include "e90canbus.h"
#include "globals.h"

const uint16_t CAN_ID = 0x0C4;
uint8_t steering_wheel_frame[7] = {0x83, 0xFD, 0xFC, 0x00, 0x00, 0xFF, 0xF1};

void canSendSteeringWheel(){
  steering_wheel_frame[1] = 0;
  steering_wheel_frame[2] = 0;

  CAN.sendMsgBuf(CAN_ID, 0, 7, steering_wheel_frame);
}
