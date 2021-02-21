#include "e90canbus.h"
#include "globals.h"

uint8_t lights_frame[3] = {0x00, 0x00, 0xf7};

const uint16_t CAN_ID = 0x21A;

void canSendLights(){
  uint16_t lights = 0;

  if(s_light_parking) lights |= L_BACKLIGHT;
  if(s_light_dip) lights |= L_DIP;
  if(s_light_main) lights |= L_MAIN;
  if(s_light_fog) lights |= L_FOG;
  
  lights_frame[0] = lights;

  CAN.sendMsgBuf(CAN_ID, 0, 3, lights_frame);
}
