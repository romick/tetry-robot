#define BUILDING_LIBRARY
#include "lib_iopins.h"
#include <pinChange.h>
const uint8_t NUM_PCINT_PINS = 8;
const IOPin* PROGMEM const PCINT_PINS[]={null,null,null,null,B4,B5,B6,B7};
PIN_CHANGE pcCallbacks[8];
