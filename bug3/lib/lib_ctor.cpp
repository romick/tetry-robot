/*
		This file has been auto-generated by WebbotLib tools V2.1
				** DO NOT MODIFY BY HAND **
*/
#include "../hardware.h"
StatusLed statusLed(&statusLED);
Switch button(&_button_);
Marquee marquee(&_marquee_);
Servo servo(&_servo_);
Servo servo2(&_servo2_);
Servo servo3(&_servo3_);
Servo servo4(&_servo4_);
Servo servo5(&_servo5_);
Servo servo6(&_servo6_);
ServoDriver Servos1(&_Servos1_);
Servo servo7(&_servo7_);
Servo servo8(&_servo8_);
Servo servo9(&_servo9_);
Servo servo10(&_servo10_);
Servo servo11(&_servo11_);
Servo servo12(&_servo12_);
ServoDriver servos2(&_servos2_);
UartHW uart1(_C_uart1);
#include <Stream/Stream.h>
NullStream nullStream;

void __attribute__ ((constructor)) _cpp_Init_(void){
	stdin = stdout = uart1;
	stderr = uart1;
}

extern "C" void __cxa_pure_virtual(void){
	while(1);
}

