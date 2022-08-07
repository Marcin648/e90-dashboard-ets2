#pragma once
#include "CanFrameBase.hpp"

class CanFrameAirbagCounter : public CanFrameBase {
private:
    can_frame frame = {0x0D7, 2, {0xC3, 0xFF}};
public:
    CanFrameAirbagCounter(MCP2515* mcp);
    void update_frame(GameTelemetry& telemetry);
    void interval_tick();
};