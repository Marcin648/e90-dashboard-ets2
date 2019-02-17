/*
  Marcin648 2019
  GNU General Public License 3.0
*/

#include <Arduino.h>

#include <stdio.h>
#include <stdint.h>
#include <mcp_can.h>
#include <SPI.h>

#include "e90canbus.h"

/*
  Setting
*/

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


/*
  Set up printf
*/
int serial_putchar(char c, FILE* f) {
    if (c == '\n') serial_putchar('\r', f);
    return Serial.write(c) == 1? 0 : 1;
}

FILE serial_stdout;

/*
  Main
*/
void setup() {
  //Initialize serial port
  Serial.begin(SERIAL_BAUD_RATE);

  //Initualize printf
  fdev_setup_stream(&serial_stdout, serial_putchar, NULL, _FDEV_SETUP_WRITE);
  stdout = &serial_stdout;

  //Initialize CAN-BUS
  while(CAN.begin(CAN_BAUD_RATE) != CAN_OK){
    printf("CAN Failed init!\n");
  }
  printf("CAN init success\n");
}

void loop() {
  canSend();
  //serialEvent();
}
