
// Include hardware info for this device	
#include <avr/io.h>

		
#include "lib_timerdef.h"
#include <timer.h>
#include <errors.h>
// Variable used by main library to link in this module
const uint8_t PROGMEM _timer_compare_error = TIMER_COMPARE_CALLBACK_EXISTS;
// The dummy routine used to denote that the compare is in use
// Only ever called from here but not static to avoid unused warnings
void nullTimerCompareCallback(const TimerCompare *timer_compare, void* data){}

// TIMER0_COMPAREA is in use
static void __attribute__ ((constructor)) init_TIMER0_COMPAREA(void){
	TimerDataCompare* data = compareGetData(TIMER0_COMPAREA);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER0_COMPAREB is in use
static void __attribute__ ((constructor)) init_TIMER0_COMPAREB(void){
	TimerDataCompare* data = compareGetData(TIMER0_COMPAREB);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER1_COMPAREA is in use
static void __attribute__ ((constructor)) init_TIMER1_COMPAREA(void){
	TimerDataCompare* data = compareGetData(TIMER1_COMPAREA);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER1_COMPAREB is in use
static void __attribute__ ((constructor)) init_TIMER1_COMPAREB(void){
	TimerDataCompare* data = compareGetData(TIMER1_COMPAREB);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER1_COMPAREC is in use
static void __attribute__ ((constructor)) init_TIMER1_COMPAREC(void){
	TimerDataCompare* data = compareGetData(TIMER1_COMPAREC);
	data->compare_callback = &nullTimerCompareCallback;
}

// Interrupt handler for  TIMER2_COMPAREA compare interrupt
ISR(TIMER2_COMPA_vect){
	__timer_compareService(TIMER2_COMPAREA);
}
// Interrupt handler for  TIMER2_COMPAREB compare interrupt
ISR(TIMER2_COMPB_vect){
	__timer_compareService(TIMER2_COMPAREB);
}
// TIMER3_COMPAREA is in use
static void __attribute__ ((constructor)) init_TIMER3_COMPAREA(void){
	TimerDataCompare* data = compareGetData(TIMER3_COMPAREA);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER3_COMPAREB is in use
static void __attribute__ ((constructor)) init_TIMER3_COMPAREB(void){
	TimerDataCompare* data = compareGetData(TIMER3_COMPAREB);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER3_COMPAREC is in use
static void __attribute__ ((constructor)) init_TIMER3_COMPAREC(void){
	TimerDataCompare* data = compareGetData(TIMER3_COMPAREC);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER4_COMPAREA is in use
static void __attribute__ ((constructor)) init_TIMER4_COMPAREA(void){
	TimerDataCompare* data = compareGetData(TIMER4_COMPAREA);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER4_COMPAREB is in use
static void __attribute__ ((constructor)) init_TIMER4_COMPAREB(void){
	TimerDataCompare* data = compareGetData(TIMER4_COMPAREB);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER4_COMPAREC is in use
static void __attribute__ ((constructor)) init_TIMER4_COMPAREC(void){
	TimerDataCompare* data = compareGetData(TIMER4_COMPAREC);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER5_COMPAREA is in use
static void __attribute__ ((constructor)) init_TIMER5_COMPAREA(void){
	TimerDataCompare* data = compareGetData(TIMER5_COMPAREA);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER5_COMPAREB is in use
static void __attribute__ ((constructor)) init_TIMER5_COMPAREB(void){
	TimerDataCompare* data = compareGetData(TIMER5_COMPAREB);
	data->compare_callback = &nullTimerCompareCallback;
}

// TIMER5_COMPAREC is in use
static void __attribute__ ((constructor)) init_TIMER5_COMPAREC(void){
	TimerDataCompare* data = compareGetData(TIMER5_COMPAREC);
	data->compare_callback = &nullTimerCompareCallback;
}

