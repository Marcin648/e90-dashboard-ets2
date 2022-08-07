#pragma once
#include <Arduino.h>
#include <stdint.h>

class StatusLed{
private:
	int pin;

	void blink(int blink_times, uint32_t delay);
public:
	StatusLed(int pin);
	void set(bool);
	void blinkSlow(int blink_times);
	void blinkFast(int blink_times);
	void fatal_loop(int blink_times);
};