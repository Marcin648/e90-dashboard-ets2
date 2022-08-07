#pragma once
#include "CanFrameBase.hpp"

class CanFrameAbs : public CanFrameBase {
private:
    can_frame frame = {0x19E, 8, {0x00, 0xE0, 0xB3, 0xFC, 0xF0, 0x43, 0x00, 0x65}};
public:
    CanFrameAbs(MCP2515* mcp);
    void update_frame(GameTelemetry& telemetry);
    void interval_tick();
};