
// Its a component of the library
#define BUILDING_LIBRARY

// Include hardware info for this device	
#include <avr/io.h>

		
	
#include <libdefs.h>	
#include <clock.h>	
		
		
#define CLOCK_PRESCALE 			1024		 
#define CLOCK_TOP 				250		 


// #define msPerTop (CLOCK_TOP*1000U*CLOCK_PRESCALE/F_CPU)
#define msPerTop 16
		 
#define usPerTop (msPerTop * 1000U)  	// convert to uS		 
static volatile TICK_COUNT wholeTicks;

		
#define CLOCK_INT_PENDING bit_is_set(TIFR0,OCF0A)		
#define CLOCK_INT_CLEAR sbi(TIFR0,OCF0A)		
		
#define CLOCK_INT_ENABLE sbi(TIMSK0,OCIE0A)		
#define CLOCK_INT_DISABLE cbi(TIMSK0,OCIE0A)		
		
#define CLOCK_TOP_REG OCR0A
#include <errors.h>		
#define STATUS_LED_PORT  PORTC		
#define STATUS_LED_INPUT PINC		
#define STATUS_LED_DDR   DDRC		
#define STATUS_LED_PIN   PC1		
static uint8_t counter;
		

void clockGetSnapshot(TIMER_SNAPSHOT* snapshot){
	// Clock timer uses TIMER_MODE_CTC_OCR which generate compare interrupts on channel A
	CRITICAL_SECTION{
		// get the current ticks from the timer
		uint8_t tcnt = TCNT0;
		// get the number of whole ticks
		snapshot->whole  = wholeTicks;
		// get the current ticks again
		snapshot->part   = TCNT0;
		// If the second reading of tcnt has gone down then there must have been an overflow
		// since reading the 'rtn' value. Or there may be a pending interrupt which may be
		// because interrupts are currently turned off. In either case increment the 'rtn' value
		// as if the interrupt has happened
		if(snapshot->part < tcnt || CLOCK_INT_PENDING ){
			snapshot->whole += usPerTop;
			// get the current ticks again
			snapshot->part = TCNT0;
		}
	}
}

TICK_COUNT clockSnapshotToTicks(const TIMER_SNAPSHOT* snapshot){
	TICK_COUNT rtn = snapshot->whole;

	// top = usPerTop
	// part     x
	TICK_COUNT frac  = snapshot->part;
	frac *= usPerTop;
	frac /= CLOCK_TOP;

	rtn += frac;

	return rtn;
}

// Get the current clock time in uS
TICK_COUNT clockGetus(void){
	TIMER_SNAPSHOT snapshot;
	clockGetSnapshot(&snapshot);

	return clockSnapshotToTicks(&snapshot);
}

// Initialise the clock timer and turn it on
void __clockInit(void){
	// Set interrupt pending = false
	CLOCK_INT_CLEAR;
	
	// Enable interrupts
	CLOCK_INT_ENABLE;
}

// ISR for clock overflow. Occurs every msPerTop
ISR(TIMER0_COMPA_vect) {
	wholeTicks += usPerTop;

	
	// Flash the status led if there is an error
	ERROR* err = &__error;
	if(err->errorCode && bit_is_set(STATUS_LED_DDR,STATUS_LED_PIN)){
		// There is an error and status led pin is an output

		// Decrement any counter
		if(counter){
			counter--;
		}
		if(counter==0){
			// Its time to do something
			if(err->remaining==0){
				err->remaining = ABS(err->errorCode);
			}

			uint8_t delay = (err->errorCode < 0 ) ? 250/msPerTop : 500/msPerTop;
			if(err->phase){
				// turn led off
				if(-- err->remaining == 0){
					delay = 2000/msPerTop;
				}
			}else{
				// turn led on
			}
			err->phase = !err->phase;
			counter = delay;
			// toggle the LED
			sbi(STATUS_LED_INPUT,STATUS_LED_PIN);
		}
	}
	
}
	