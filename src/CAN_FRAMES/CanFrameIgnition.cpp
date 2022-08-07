#include "CAN_FRAMES/CanFrameIgnition.hpp"

CanFrameIgnation::CanFrameIgnation(MCP2515* mcp) : CanFrameBase(mcp) {
    this->final_frame = &frame_on;
    this->interval = 10;
}

void CanFrameIgnation::update_frame(GameTelemetry& telemetry){
    if(telemetry.ignition){
        this->final_frame = &frame_on;
    }else{
        this->final_frame = &frame_off;
    }
}

void CanFrameIgnation::interval_tick(){
    this->send();
    this->frame_on.data[4]++;
    this->frame_off.data[4]++;
}