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
#include "configuration.h"

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