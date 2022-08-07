#include "StatusLed.hpp"

StatusLed::StatusLed(int pin){
    this->pin = pin;
    pinMode(pin, OUTPUT);
}

void StatusLed::set(bool on){
    digitalWrite(this->pin, on ? HIGH : LOW);
}

void StatusLed::blink(int blink_times, uint32_t blink_delay){
    for(int i = 0; i < blink_times; i++){
        digitalWrite(this->pin, HIGH);
        delay(blink_delay);
        digitalWrite(this->pin, LOW);
        delay(blink_delay);
    }
}

void StatusLed::blinkSlow(int blink_times){
    this->blink(blink_times, 500);
}

void StatusLed::blinkFast(int blink_times){
    this->blink(blink_times, 100);
}

void StatusLed::fatal_loop(int blink_times){
    for(;;){
        this->blinkSlow(blink_times);
        delay(5000);
    }
}