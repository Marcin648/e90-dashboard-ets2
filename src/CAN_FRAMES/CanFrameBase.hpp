#pragma once
#include <stdint.h>
#include <mcp2515.h>
#include "GameTelemetry.hpp"

class CanFrameBase{
protected:
	MCP2515* mcp;
	can_frame* final_frame;
	uint32_t interval;
	uint32_t last_time;
public:
	CanFrameBase(MCP2515* mcp);
	MCP2515::ERROR send();

	virtual void update_frame(GameTelemetry& telemetry) {};
	virtual void interval_tick() {};
	void update();
};