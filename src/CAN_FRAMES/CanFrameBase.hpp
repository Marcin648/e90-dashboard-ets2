#pragma once
#include <stdint.h>
#include <mcp2515.h>
#include "GameTelemetry.hpp"

class CanFrameBase{
private:
	can_frame frame;
	uint32_t interval;
	uint32_t last_time;
public:
	CanFrameBase(uint32_t id, uint8_t data_lenght, uint32_t interval);

	MCP2515::ERROR send(MCP2515& mcp);

	virtual void update_frame(GameTelemetry& telemetry);
	void update();	
};