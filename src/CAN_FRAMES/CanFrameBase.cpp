#include "CanFrameBase.hpp"

CanFrameBase::CanFrameBase(uint32_t id, uint8_t data_lenght, uint32_t interval){
    this->frame.can_id = id;
    this->frame.can_dlc = data_lenght;
    this->interval = interval;
    this->last_time = millis();
}

MCP2515::ERROR CanFrameBase::send(MCP2515& mcp){
    return mcp.sendMessage(&this->frame);
}

void CanFrameBase::update(){
    uint32_t courent_time = millis();
    if(courent_time - this->last_time > this->interval){
        last_time = courent_time;
    }
}