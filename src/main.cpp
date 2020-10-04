/*
  Marcin648 2019
  GNU General Public License 3.0
*/

#include <Arduino.h>

#include <PacketSerial.h>
#include <mcp_can.h>
#include <SPI.h>

#include "e90canbus.h"
#include "serial.h"

/*
  Setting
*/
//Delta time multiple
// 2 - speed scale in mph
// 3 - speed scale in km/h
const uint8_t DTIME_MULTIPLE = 3;

//Serial boud rate
const uint32_t SERIAL_BAUD_RATE = 115200;

//CAN-BUS boud rate
const int CAN_BAUD_RATE = CAN_100KBPS;

//SPI CS PIN
const int SPI_CS_PIN = 9;

/*
  Set up can bus
*/
MCP_CAN CAN(SPI_CS_PIN);

PacketSerial serial;

/*
  Main
*/
void setup() {
  //Initialize serial port
  serial.begin(SERIAL_BAUD_RATE);
  serial.setPacketHandler(&serialReceive);

  //Initialize CAN-BUS
  while(CAN.begin(CAN_BAUD_RATE) != CAN_OK){
    delay(100);
  }
}

void loop() {
  canSend();
  serial.update();
}