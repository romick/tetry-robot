#define BUILDING_LIBRARY
#include <avr/io.h>
#include <libdefs.h>
#include <timer.h>
extern const PROGMEM Timer PROGMEM pgm_Timers[];
void __initTimers(void){
 
// Set Timer0 to the following:-
//		Mode 	 = TIMER_MODE_CTC_OCR
//		Prescale = 1024
	// Save the timer mode
	timerGetData(&pgm_Timers[0])->mode = TIMER_MODE_CTC_OCR;
	// Set the timer mode
	
	// Mode TIMER_MODE_CTC_OCR is 2
	// Assume current mode settings are all 0	
		
			
	if(2 & 1){
		sbi(TCCR0A,WGM00);
	} 
		
			
	if(2 & 2){
		sbi(TCCR0A,WGM01);
	} 
		
			
	if(2 & 4){
		sbi(TCCR0B,WGM02);
	} 
		
	// Top is stored in Compare A OCR
				OCR0A = 250;			
				
	// Turn on the timer by setting prescaler
	timerGetData(&pgm_Timers[0])->prescale_value = 1024;
	TCCR0B |= 5;
	 
// Set Timer1 to the following:-
//		Mode 	 = TIMER_MODE_PWM_FAST_ICR
//		Prescale = 8
	// Save the timer mode
	timerGetData(&pgm_Timers[1])->mode = TIMER_MODE_PWM_FAST_ICR;
	// Set the timer mode
	
	// Mode TIMER_MODE_PWM_FAST_ICR is 14
	// Assume current mode settings are all 0	
		
			
	if(14 & 1){
		sbi(TCCR1A,WGM10);
	} 
		
			
	if(14 & 2){
		sbi(TCCR1A,WGM11);
	} 
		
			
	if(14 & 4){
		sbi(TCCR1B,WGM12);
	} 
		
			
	if(14 & 8){
		sbi(TCCR1B,WGM13);
	} 
		
	// Top is stored in ICR register
	ICR1 = 40000;			
			
	// Turn on the timer by setting prescaler
	timerGetData(&pgm_Timers[1])->prescale_value = 8;
	TCCR1B |= 2;
	 
// Set Timer3 to the following:-
//		Mode 	 = TIMER_MODE_PWM_FAST_ICR
//		Prescale = 8
	// Save the timer mode
	timerGetData(&pgm_Timers[3])->mode = TIMER_MODE_PWM_FAST_ICR;
	// Set the timer mode
	
	// Mode TIMER_MODE_PWM_FAST_ICR is 14
	// Assume current mode settings are all 0	
		
			
	if(14 & 1){
		sbi(TCCR3A,WGM30);
	} 
		
			
	if(14 & 2){
		sbi(TCCR3A,WGM31);
	} 
		
			
	if(14 & 4){
		sbi(TCCR3B,WGM32);
	} 
		
			
	if(14 & 8){
		sbi(TCCR3B,WGM33);
	} 
		
	// Top is stored in ICR register
	ICR3 = 40000;			
			
	// Turn on the timer by setting prescaler
	timerGetData(&pgm_Timers[3])->prescale_value = 8;
	TCCR3B |= 2;
	 
// Set Timer4 to the following:-
//		Mode 	 = TIMER_MODE_PWM_FAST_ICR
//		Prescale = 8
	// Save the timer mode
	timerGetData(&pgm_Timers[4])->mode = TIMER_MODE_PWM_FAST_ICR;
	// Set the timer mode
	
	// Mode TIMER_MODE_PWM_FAST_ICR is 14
	// Assume current mode settings are all 0	
		
			
	if(14 & 1){
		sbi(TCCR4A,WGM40);
	} 
		
			
	if(14 & 2){
		sbi(TCCR4A,WGM41);
	} 
		
			
	if(14 & 4){
		sbi(TCCR4B,WGM42);
	} 
		
			
	if(14 & 8){
		sbi(TCCR4B,WGM43);
	} 
		
	// Top is stored in ICR register
	ICR4 = 40000;			
			
	// Turn on the timer by setting prescaler
	timerGetData(&pgm_Timers[4])->prescale_value = 8;
	TCCR4B |= 2;
	 
// Set Timer5 to the following:-
//		Mode 	 = TIMER_MODE_PWM_FAST_ICR
//		Prescale = 8
	// Save the timer mode
	timerGetData(&pgm_Timers[5])->mode = TIMER_MODE_PWM_FAST_ICR;
	// Set the timer mode
	
	// Mode TIMER_MODE_PWM_FAST_ICR is 14
	// Assume current mode settings are all 0	
		
			
	if(14 & 1){
		sbi(TCCR5A,WGM50);
	} 
		
			
	if(14 & 2){
		sbi(TCCR5A,WGM51);
	} 
		
			
	if(14 & 4){
		sbi(TCCR5B,WGM52);
	} 
		
			
	if(14 & 8){
		sbi(TCCR5B,WGM53);
	} 
		
	// Top is stored in ICR register
	ICR5 = 40000;			
			
	// Turn on the timer by setting prescaler
	timerGetData(&pgm_Timers[5])->prescale_value = 8;
	TCCR5B |= 2;
	}
