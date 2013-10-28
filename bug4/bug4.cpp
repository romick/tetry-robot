#define UART_RX_BUFFER_SIZE = 160;

#include "hardware.h"

#include <string.h>
// Initialise the hardware

//Data protocol is trying to be SSC32 servo controller compatible.
//At the moment only the following commands implemented:
//    - servo group movement
//For the protocol details please refer to SSC32 protocol description: http://www.lynxmotion.com/images/html/build136.htm

#define SERVOS_NUMBER 11  
//actually 12 counting 0 as first 
#define SSC_RESOLUTION 1000
#define DEBUG_SESSION 1
#define MY_DRIVE_SPEED_MIN 500
#define MY_DRIVE_SPEED_MAX 2500
#define MY_DRIVE_SPEED_AVERAGE 1500

Servo* servos[SERVOS_NUMBER];

uint8_t VERBOSE = 0;

struct command {
	uint8_t has_changed[SERVOS_NUMBER];
	float servo_target_positions[SERVOS_NUMBER];
	float servo_current_positions[SERVOS_NUMBER];
	float servo_speeds[SERVOS_NUMBER];
	float servo_speed_per_tick[SERVOS_NUMBER];
	int16_t time;
};

struct command command_receiving;

struct command command_in_process;

char r_curr_subcommand;
int8_t r_curr_servo;

TICK_COUNT last_loop_time;

void initialize_command (struct command* command) {
	(*command).time = 1;
	for(int16_t i=0;i<=SERVOS_NUMBER;i++) {
		(*command).has_changed[i]=0;
		(*command).servo_target_positions[i]=MY_DRIVE_SPEED_AVERAGE;
		(*command).servo_current_positions[i]=MY_DRIVE_SPEED_AVERAGE;
		(*command).servo_speeds[i]=10;
		(*command).servo_speed_per_tick[i]=100;
	}
}


void print_command (struct command* command, TICK_COUNT loop_number) {
	if (loop_number) {
		cout << "Loop " << loop_number << "\n";
	}
	cout << "command:\nTime to execute: " << (*command).time << "\r\n";
	int8_t ia;
	for (ia=0; ia <= SERVOS_NUMBER; ia++) {
		cout << "#" << ia << " Changed?:" << (*command).has_changed[ia] << " Trgt: " << (*command).servo_target_positions[ia] << "\n";    //: Current pos: " << (*command).servo_current_positions[ia] << " Speed: " << (*command).servo_speeds[ia] << " Spt: " << (*command).servo_speed_per_tick[ia] << "\n";
	}
}


int to_int (char chr) {
	int i = chr - '0';
	if (VERBOSE==1) {
		cout << "\n To_int'd number:" << i << "\n";
	}
	return i;
}




// Initialise the hardware
void appInitHardware(void) {
	initHardware();
	servos[0] = &servo;
	servos[1] = &servo2;
	servos[2] = &servo3;
	servos[3] = &servo4;
	servos[4] = &servo5;
	servos[5] = &servo6;
	servos[6] = &servo7;
	servos[7] = &servo8;
	servos[8] = &servo9;
	servos[9] = &servo10;
	servos[10] = &servo11;
	servos[11] = &servo12;
	initialize_command(&command_receiving);
	initialize_command(&command_in_process);
}
// Initialise the software
TICK_COUNT appInitSoftware(TICK_COUNT loopStart){
	return 0;
}

// This is the main loop
TICK_COUNT appControl(LOOP_COUNT loopCount, TICK_COUNT loopStart) {

	int early_break = FALSE;
	while ((uart1.isRxBufferEmpty()==FALSE) && (early_break == FALSE)) {
		char data = uart1.read();
		if (data != EOF) {
			cout << data;
		}
		switch (data) {
			case '?':
			{
				
				//subcommand "Toggle verbose TRUE/FALSE" 
				if (VERBOSE==0) {
					VERBOSE = 1;
					int8_t i;
					for (i=0; i <= SERVOS_NUMBER; i++) {
						cout << "Current speed:" << (*servos[i]).getSpeed() << "\n";
					}
				} else {
					VERBOSE = 0;
				}
				break;
			}
			case '#':
			{
				//subcommand "Servo number"
				r_curr_servo = 0;
				r_curr_subcommand = data;
				if (VERBOSE==1) {
					cout << "Received servo number command \n";
				}
				break;
			}
			case 'P':
			{
				//subcommand "Position"
				command_receiving.servo_target_positions[r_curr_servo] = 0;
				r_curr_subcommand = data;
				if (VERBOSE==1) {
					cout << "Received position command \n";
				}
				break;
			}
			case 'S':
			{
				//subcommand "Speed"
				command_receiving.servo_speeds[r_curr_servo] = 0;
				r_curr_subcommand = data;
				if (VERBOSE==1) {
					cout << "Received speed command \n";
				}
				break;
			}
			case 'T':
			{
				//subcommand "Time"
				command_receiving.time = 0;
				r_curr_subcommand = data;
				if (VERBOSE==1) {
					cout << "Received time command \n";
				}
				break;
			}
			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
			case '8':
			case '9':
			case '0':
			{
				if (VERBOSE==1) {
					cout << "Received digit \n Current subcommand is " << r_curr_subcommand << "\n";
				}
				switch (r_curr_subcommand) {
					case '#':
					{
						r_curr_servo = r_curr_servo*10 + to_int(data);
						if (VERBOSE==1) {
							cout << "Set current servo to:" << r_curr_servo << "\n";
						}
						break;
					}
					case 'P':
					{
						command_receiving.servo_target_positions[r_curr_servo] = command_receiving.servo_target_positions[r_curr_servo]*10 + to_int(data);
						command_receiving.has_changed[r_curr_servo] = 1;
						if (VERBOSE==1) {
							cout << "Set current servo target position to:" << command_receiving.servo_target_positions[r_curr_servo] << "\n";
						}
						break;
					}
					case 'S':
					{
						command_receiving.servo_speeds[r_curr_servo] = command_receiving.servo_speeds[r_curr_servo]*10 + to_int(data);
						if (VERBOSE==1) {
							cout << "Set current servo speed to:" << command_receiving.servo_speeds[r_curr_servo] << "\n";
						}
						break;
					}
					case 'T':
					{
						command_receiving.time = command_receiving.time*10 + to_int(data);
						if (VERBOSE==1) {
							cout << "Set movement time to:" << command_receiving.time << "\n";
						}
						break;
					}
					default:
					{
						//err.print "reader: No current command defined!";
						break;
					}
				}
				break;
			}
			case ' ':
			{
				r_curr_subcommand = ' ';
				break;
			}
			case '\r':
			case '\n':
			{
				// execute command
				r_curr_subcommand = ' ';
				
				
				int8_t jl=0;
				for (jl=0; jl <= SERVOS_NUMBER; jl++) {
					if (command_receiving.has_changed[jl] > 0) {
						command_in_process.has_changed[jl] = 1;
						command_in_process.servo_target_positions[jl] = command_receiving.servo_target_positions[jl];
					}
					
				}


				initialize_command(&command_receiving);
				
				if (VERBOSE==1) {
					cout << "After copy.\nReceived ";
					print_command(&command_receiving, NULL);
					cout << "In process ";
					print_command(&command_in_process, NULL);
				}
				
				//Stop parsing RX buffer and go straight to command execution, the rest of buffer will be parsed in next main loop
				early_break = TRUE;

				break;
			}
			default:
			{
				break;
			}
		}

	}

	if (loopStart > (last_loop_time + SSC_RESOLUTION)) {   
		last_loop_time = loopStart;

		int8_t jk=0;
		for (jk=0; jk <= SERVOS_NUMBER; jk++) {
			DRIVE_SPEED speed = interpolate((int16_t)command_in_process.servo_target_positions[jk], MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX, DRIVE_SPEED_MIN,DRIVE_SPEED_MAX);
			(*servos[jk]).setSpeed(speed);  
			command_in_process.has_changed[jk] = 0;
			command_in_process.servo_current_positions = (*servos[jk]).getSpeed();
				// cout << "#" << jk << " Chgd?:" << command_in_process.has_changed[jk] << " Trgt:" << speed << "\n";
		}
		
	}
	return 0;
}
