#include "e90canbus.h"
#include "globals.h"

const uint16_t CAN_ID = 0x1A6;
uint8_t speed_frame[8] = {0x13, 0x4D, 0x46, 0x4D, 0x33, 0x4D, 0xD0, 0xFF};

uint16_t last_speed_value = 0;
void canSendSpeed(){
  const uint8_t delta_time = 100; // const
  uint16_t speed_value = s_speed + last_speed_value;

  uint16_t counter = (speed_frame[6] | (speed_frame[7] << 8)) & 0x0FFF;
  counter += (float)delta_time * M_PI;

  speed_frame[0] = speed_value;
  speed_frame[1] = (speed_value >> 8);

  speed_frame[2] = speed_frame[0];
  speed_frame[3] = speed_frame[1];

  speed_frame[4] = speed_frame[0];
  speed_frame[5] = speed_frame[1];

  speed_frame[6] = counter;
  speed_frame[7] = (counter >> 8) | 0xF0;

  CAN.sendMsgBuf(CAN_ID, 0, 8, speed_frame);
  last_speed_value = speed_value;
}
