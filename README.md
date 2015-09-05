tetry-robot
===========

A robot project consisting of Axon-driven, custom-made, four-legs servo-platform (C, C++, Webbotlib) and PC/MAC controlling app (Python for bot logic, wxPython for GUI).

Special thanks to:
 - Rob Cook for his IK algorithm. (http://robcook.eu/hexy/inverse-kinematics-part-1/)
 - admin@societyofrobots.com for his Axon II robot controller (http://www.societyofrobots.com/axon2/)
 - webbot@webbot.org.uk for Webbotlib library  (http://webbot.org.uk/iPoint/30.page)
 - wxPython project contributors for wxPython GUI framework (http://www.wxpython.org/)
 - PySerial project contributors (http://pyserial.sourceforge.net/)
  
 
Required:
python:
 - flask
 - setproctitle
 - numpy
socat (for testing purposes)

Architecture:
 - using reactive python scripts based on PubSub and RPC messages
 - crossbar.io is a transport for messages
 - one folder is one microservice
 
Start by running ./start.sh