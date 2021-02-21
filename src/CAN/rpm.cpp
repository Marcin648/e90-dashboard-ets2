#include "e90canbus.h"
#include "globals.h"

const uint16_t CAN_ID = 0x0AA;
uint8_t rpm_frame[8] = {0x5F, 0x59, 0xFF, 0x00, 0x34, 0x0D, 0x80, 0x99};

void canSendRPM(){
  uint16_t value = s_rpm * 4;

  rpm_frame[4] = value;
  rpm_frame[5] = (value >> 8);

  CAN.sendMsgBuf(CAN_ID, 0, 8, rpm_frame);
}
