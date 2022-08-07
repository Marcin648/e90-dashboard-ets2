#include "CAN_FRAMES/CanFrameAbs.hpp"

CanFrameAbs::CanFrameAbs(MCP2515* mcp) : CanFrameBase(mcp) {
    this->final_frame = &frame;
    this->interval = 200;
}

void CanFrameAbs::update_frame(GameTelemetry& telemetry){
    ;
}

void CanFrameAbs::interval_tick(){
    this->frame.data[2] = ((((this->frame.data[2] >> 4) + 3) << 4) & 0xF0) | 0x03;
    this->send();
}