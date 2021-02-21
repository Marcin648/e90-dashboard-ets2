#include "e90canbus.h"
#include "globals.h"

const uint16_t CAN_ID = 0x1A6;
uint8_t speed_frame[8] = {0x13, 0x4D, 0x46, 0x4D, 0x33, 0x4D, 0xD0, 0xFF};

uint16_t lastSpeed = 0;
void canSendSpeed(){
  const uint8_t deltaTime = 100; // const
  uint16_t speedValue = s_speed + lastSpeed;

  uint16_t counter = (speed_frame[6] | (speed_frame[7] << 8)) & 0x0FFF;
  counter += deltaTime * DTIME_MULTIPLE;

  speed_frame[0] = speedValue;
  speed_frame[1] = (speedValue >> 8);

  speed_frame[2] = speed_frame[0];
  speed_frame[3] = speed_frame[1];

  speed_frame[4] = speed_frame[0];
  speed_frame[5] = speed_frame[1];

  speed_frame[6] = counter;
  speed_frame[7] = (counter >> 8) | 0xF0;

  CAN.sendMsgBuf(CAN_ID, 0, 8, speed_frame);
  lastSpeed = speedValue;
}
