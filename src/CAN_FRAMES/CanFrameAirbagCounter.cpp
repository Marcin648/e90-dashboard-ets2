#include "CAN_FRAMES/CanFrameAirbagCounter.hpp"

CanFrameAirbagCounter::CanFrameAirbagCounter(MCP2515* mcp) : CanFrameBase(mcp) {
    this->final_frame = &frame;
    this->interval = 200;
}

void CanFrameAirbagCounter::update_frame(GameTelemetry& telemetry){
    ;
}

void CanFrameAirbagCounter::interval_tick(){
    this->send();
    this->frame.data[0]++;
}