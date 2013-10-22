
// Its a component of the library
#define BUILDING_LIBRARY

// Include hardware info for this device	
#include <avr/io.h>

		
	
#include <libdefs.h>	
#include <clock.h>	
#include <scheduler.h>	


// Define the structure to hold one job
typedef struct s_job{
	boolean				used;		// is this slot in use?
	SchedulerCallback	callback;	// The routine to callback
	volatile SchedulerData		data;// The data for the callback
	TICK_COUNT			delay;		// The delay required in us
	TICK_COUNT			start;		// The start of the delay
} JOB;


		
		

#ifndef SCHEDULER_MAX_JOBS
#define SCHEDULER_MAX_JOBS 1
#endif

// The maximum number of concurrent jobs that can be scheduled
uint8_t maxJobs = SCHEDULER_MAX_JOBS;

// Create the queue of jobs
static JOB __queue[SCHEDULER_MAX_JOBS];


#define CLOCK_PRESCALE 			1024		 
#define CLOCK_TOP 				250
#define SCHEDULER_INT_PENDING bit_is_set(TIFR0,OCF0B)		
#define SCHEDULER_INT_CLEAR sbi(TIFR0,OCF0B)		
		
#define SCHEDULER_INT_ENABLE sbi(TIMSK0,OCIE0B)		
#define SCHEDULER_INT_DISABLE cbi(TIMSK0,OCIE0B)		
		
#define SCHEDULER_THRESHOLD OCR0B
#define CLOCK_COUNTER TCNT0		
		
// Is the scheduler execution loop running
static volatile boolean __running; //=FALSE;

// If we are running - is the list dirty
static volatile boolean __recheck; //=FALSE;

// The number of scheduled jobs
static volatile int __numJobs;

// Calculate the required compare threshold to cause an interrupt at the required time
static uint16_t calcTicks(TICK_COUNT us){
	TICK_COUNT ticks = us * (F_CPU / (CLOCK_PRESCALE * 1000000));
	uint16_t rtn = MIN(ticks,CLOCK_TOP);
	return rtn;
}

// called under compare interrupts when there is something in the queue
static void __scheduleUpdate(void){
	// Dont call me again - turn off compare interrupts
	SCHEDULER_INT_DISABLE;

	// Turn interrupts back on
	INTERRUPTABLE_SECTION{
		__running = TRUE;
		TICK_COUNT lowest;
		do{
			int slot;
			__recheck = FALSE;
			JOB* job;
			lowest=0;
			for(slot=maxJobs-1, job=&__queue[slot]; slot>=0; slot--, job--){
				if(job->used){
					// check if time has elapsed
					TICK_COUNT overflow;	// how many us the timer has overshot when it should have happened
					TICK_COUNT start=job->start;
					TICK_COUNT delay=job->delay;
					if(clockHasElapsedGetOverflow(start, delay, &overflow)){
						SchedulerCallback callback = job->callback;
						SchedulerData data = job->data;

						// Mark this job as unused. No more references shoud be made to job->xxxx
						job->used = FALSE;
						--__numJobs;

						// Run the job with interrupts enabled
						callback(data,start+delay,overflow);


						// Force another loop as the time taken may mean
						// something else can now run
						__recheck = TRUE;
					}else{
					   // overflow has the remaining number of microseconds to wait
					   if(lowest==0 || overflow < lowest){
						   lowest = overflow;
					   }
					}
				}
			}
		}while( __recheck);
		__running=FALSE;

		if(__numJobs > 0){
			// Decide when we need to interrupt again
			uint16_t compare = calcTicks(lowest) + CLOCK_COUNTER;
			while(compare >= CLOCK_TOP){
				compare -= CLOCK_TOP;
			}
			// Set when next interrupt should occur
			SCHEDULER_THRESHOLD = compare;
			// Clear any pending interrupt
			SCHEDULER_INT_CLEAR;
			// Look for new interrupts
			SCHEDULER_INT_ENABLE;
		}

	} // Restore previous interrupt enable
}

// schedule a new job
// callback Is the function to be run at a later date
// data is a block of data to be passed into the callback
// start (in us) Is the start time of the delay
// delay (in us) Is the amount to delay by
void scheduleJob(SchedulerCallback callback, SchedulerData data, TICK_COUNT start, TICK_COUNT delay){
	boolean doItNow = FALSE;

 	if(delay < 1000U){
		// it needs to happen now as the delay is less than the heartbeat timer interrupt of 1ms
		if(__running){
			// make sure we do another loop of __scheduleUpdate to find it
			__recheck=TRUE;
		}else{
			// scheduler is dormant so just do it now
			doItNow = TRUE;
		}
	}

	if(!doItNow){
		int slot;
		// queue it up
		boolean found=FALSE;
		CRITICAL_SECTION{
			for(slot=0; slot < maxJobs; slot++){
				JOB* job = &__queue[slot];
				if(!job->used){
					job->used = TRUE;
					job->callback = callback;
					job->data = data;
					job->start=start;
					job->delay=delay;
					found=TRUE;
					__numJobs++;
					break;
				}
			}
		}

		if(!found){
			// the queue is exhausted
			setError(SCHEDULER_EXHAUSTED);
			doItNow = TRUE;
		}
	}



	if(doItNow){
		// we need to do it now
		TICK_COUNT overflow;

		// wait for expiry
		while(!clockHasElapsedGetOverflow(start, delay, &overflow));

		// call the queued routine
		callback(data,start+delay,overflow);
	}else{
		if(!__running){
			__scheduleUpdate();
		}
	}
}



// ISR for scheduler match - check if another job needs to run
ISR(TIMER0_COMPB_vect) {
	__scheduleUpdate();
}
	