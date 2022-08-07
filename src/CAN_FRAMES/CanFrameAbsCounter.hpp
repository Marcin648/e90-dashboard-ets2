#pragma once
#include "CanFrameBase.hpp"

class CanFrameAbsCounter : public CanFrameBase {
private:
    can_frame frame = {0x0C0, 2, {0xF0, 0xFF}};
public:
    CanFrameAbsCounter(MCP2515* mcp);
    void update_frame(GameTelemetry& telemetry);
    void interval_tick();
};