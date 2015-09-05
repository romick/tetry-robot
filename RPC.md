List of RPCs
============

com.tetry.queue.get_next
------------------------
Description:
 returns next command in queue of commands to be sent to servos

Parameters:
 None

Result:
 ... to define!!!

com.tetry.queue.append
------------------------
Description:
 append a command to the queue of commands to be sent to servos

Parameters:
 ... to define!!!

Result:
 None

com.tetry.convert_command
-------------------------
Description:
 gets a list of servo angles and returns appropriate serial command, based on protocol set in physical model

Parameters:
 - bot_command
    ... to define!!!

Result:
 - text message to send to hardware

com.tetry.send2ssc32
--------------------
Description:
 gets a text command to be sent to com port of ssc32 and sends it

Parameters:
 - command - text

Result:
 None

com.tetry.dummy
---------------
Description:

Parameters:

Result:

