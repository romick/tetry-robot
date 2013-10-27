#include "../hardware.h"
static const char PROGMEM name_button[] = "button";
static const char PROGMEM name_uart1[] = "uart1";
static const char PROGMEM name_led_display[] = "led_display";
static const char PROGMEM name_marquee[] = "marquee";
static const char PROGMEM name_servo[] = "servo";
static const char PROGMEM name_servo2[] = "servo2";
static const char PROGMEM name_servo3[] = "servo3";
static const char PROGMEM name_servo4[] = "servo4";
static const char PROGMEM name_servo5[] = "servo5";
static const char PROGMEM name_servo6[] = "servo6";
static const char PROGMEM name_Servos1[] = "Servos1";
static const char PROGMEM name_servo7[] = "servo7";
static const char PROGMEM name_servo8[] = "servo8";
static const char PROGMEM name_servo9[] = "servo9";
static const char PROGMEM name_servo10[] = "servo10";
static const char PROGMEM name_servo11[] = "servo11";
static const char PROGMEM name_servo12[] = "servo12";
static const char PROGMEM name_servos2[] = "servos2";
static const char PROGMEM unknown[] = "?";

#define NUM_DEVICES 18
static const void* PROGMEM const tbl[]={
	&_button_, name_button,
	&__C_uart1, name_uart1,
	&_led_display_, name_led_display,
	&_marquee_, name_marquee,
	&_servo_, name_servo,
	&_servo2_, name_servo2,
	&_servo3_, name_servo3,
	&_servo4_, name_servo4,
	&_servo5_, name_servo5,
	&_servo6_, name_servo6,
	&_Servos1_, name_Servos1,
	&_servo7_, name_servo7,
	&_servo8_, name_servo8,
	&_servo9_, name_servo9,
	&_servo10_, name_servo10,
	&_servo11_, name_servo11,
	&_servo12_, name_servo12,
	&_servos2_, name_servos2
	};

const char* getDeviceName(const void* device){
	const char* rtn = unknown;
	for(int i=0 ; i<NUM_DEVICES*2; i+=2){
		const void* addr = (const void*)pgm_read_word(&tbl[i]);
		if( addr == device){
			rtn = (const void*)pgm_read_word(&tbl[i+1]);
		}
	}
	return rtn;
}
