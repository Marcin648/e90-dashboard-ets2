#pragma once
#include <stdint.h>
#include <mcp_can_dfs.h>

/*
    Serial
*/
//Serial boud rate
const uint32_t SERIAL_BAUD_RATE = 115200;

/*
    CAN
*/
//CAN-BUS boud rate
const int CAN_BAUD_RATE = CAN_100KBPS;

//SPI CS PIN
const int SPI_CS_PIN = 9;


/*
    Dashboard
*/
//Delta time multiple
// 2 - speed scale in mph
// 3 - speed scale in km/h
const uint8_t DTIME_MULTIPLE = 3;



