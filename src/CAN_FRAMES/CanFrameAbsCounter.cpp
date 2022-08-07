#include "CAN_FRAMES/CanFrameAbsCounter.hpp"

CanFrameAbsCounter::CanFrameAbsCounter(MCP2515* mcp) : CanFrameBase(mcp) {
    this->final_frame = &frame;
    this->interval = 200;
}

void CanFrameAbsCounter::update_frame(GameTelemetry& telemetry){
    ;
}

void CanFrameAbsCounter::interval_tick(){
    this->send();
    this->frame.data[0] = ((this->frame.data[0] + 1) | 0xF0);
}