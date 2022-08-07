#pragma once
#include "CanFrameBase.hpp"

class CanFrameIgnation : public CanFrameBase {
private:
    can_frame frame_on = {0x130, 5, {0x45, 0x42, 0x69, 0x8f, 0xE2}};
    can_frame frame_off = {0x130, 5, {0x00, 0x00, 0xC0, 0x0f, 0xE2}}; 
public:
    CanFrameIgnation(MCP2515* mcp);
    void update_frame(GameTelemetry& telemetry);
    void interval_tick();
};