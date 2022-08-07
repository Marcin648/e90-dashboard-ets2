#include "CAN_FRAMES/CanFrameBase.hpp"

CanFrameBase::CanFrameBase(MCP2515* mcp){
    this->mcp = mcp;
    this->last_time = millis();
}

MCP2515::ERROR CanFrameBase::send(){
    return this->mcp->sendMessage(this->final_frame);
}

void CanFrameBase::update(){
    uint32_t courent_time = millis();
    if(courent_time - this->last_time > this->interval){
        this->interval_tick();
        this->last_time = courent_time;
    }
}