#include "e90canbus.h"
#include "globals.h"

const uint16_t CAN_ID = 0x39E;
uint8_t time_frame[8] = {0x0B, 0x10, 0x00, 0x0D, 0x1F, 0xDF, 0x07, 0xF2};

void canSendTime(){
  time_frame[0] = s_time_hour;
  time_frame[1] = s_time_minute;
  time_frame[2] = s_time_sec;

  time_frame[3] = s_time_day;
  time_frame[4] = (s_time_month << 4) | 0x0F;

  time_frame[5] = (uint8_t)s_time_year;
  time_frame[6] = (uint8_t)(s_time_year >> 8);
  CAN.sendMsgBuf(CAN_ID, 0, 8, time_frame);
}
