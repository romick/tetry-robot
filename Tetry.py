
import legIK
import time
import math

class Robot:
	"""Tetrym
	
	 legFL   --##--  legFR
	           ##
	 legBL   --##--  legBR


	"""
	def __init__(self, *arg, **kwds):
	        self.legFR = legIK.leg(offset=[25,25],   coxa=45, temur=45, tibia=85, servos=[0,1,2])
	        self.legFL = legIK.leg(offset=[-25,25],  coxa=45, temur=45, tibia=85, servos=[3,4,5])
	        self.legBR = legIK.leg(offset=[25,-25],  coxa=45, temur=45, tibia=85, servos=[6,7,8])
	        self.legBL = legIK.leg(offset=[-25,-25], coxa=45, temur=45, tibia=85, servos=[9,10,11])
	        self.sender = kwds['sender']

	        self.initBot()


	def initBot(self):
			self._send(self.legFR.gCExactCoordinates(75,75,40)+self.legFL.gCExactCoordinates(-75,75,40)+self.legBR.gCExactCoordinates(75,-75,40)+self.legBL.gCExactCoordinates(-75,-75,40))

	def makeStep(self, angle):
			

			angle = math.radians(angle)
			
			s,t = math.sin(angle)*5, math.cos(angle)*5

			print "Offsets are: %f, %f" % (s,t)

			d=10
			sleep1=0.1
			sleep2=0.2

			#assume to start from BasePose
			#raise Front Right leg , move forward by 20mm, lower it, then move body forward by 5mm
			self._send(self.legFR.gCOffset(s,  t, -d))
			time.sleep(sleep1)
			self._send(self.legFR.gCOffset(s*2, t*2, 0))
			time.sleep(sleep1)
			self._send(self.legFR.gCOffset(s,  t, d))
			time.sleep(sleep1)
			self._send(self.legFR.gCOffset(-s, -t, 0) + self.legFL.gCOffset(-s, -t, 0) + self.legBR.gCOffset(-s, -t, 0) + self.legBL.gCOffset(-s, -t, 0))
			time.sleep(sleep2)

			#raise Back Left leg , move forward by 20mm, lower it, then move body forward by 5mm
			self._send(self.legBL.gCOffset(s,  t, -d))
			time.sleep(sleep1)
			self._send(self.legBL.gCOffset(s*2, t, 0))
			time.sleep(sleep1)
			self._send(self.legBL.gCOffset(s,  t, d))
			time.sleep(sleep1)
			self._send(self.legFR.gCOffset(-s, -t, 0) + self.legFL.gCOffset(-s, -t, 0) + self.legBR.gCOffset(-s, -t, 0) + self.legBL.gCOffset(-s, -t, 0))
			time.sleep(sleep2)

			#raise Front Left leg , move forward by 20mm, lower it, then move body forward by 5mm
			self._send(self.legFL.gCOffset(s,  t, -d))
			time.sleep(sleep1)
			self._send(self.legFL.gCOffset(s*2, t, 0))
			time.sleep(sleep1)
			self._send(self.legFL.gCOffset(s,  t, d))
			time.sleep(sleep1)
			self._send(self.legFR.gCOffset(-s, -t, 0) + self.legFL.gCOffset(-s, -t, 0) + self.legBR.gCOffset(-s, -t, 0) + self.legBL.gCOffset(-s, -t, 0))
			time.sleep(sleep2)

			#raise Back Right leg , move forward by 20mm, lower it, then move body forward by 5mm
			self._send(self.legBR.gCOffset(s,  t, -d))
			time.sleep(sleep1)
			self._send(self.legBR.gCOffset(s*2, t, 0))
			time.sleep(sleep1)
			self._send(self.legBR.gCOffset(s,  t, d))
			time.sleep(sleep1)
			self._send(self.legFR.gCOffset(-s, -t, 0) + self.legFL.gCOffset(-s, -t, 0) + self.legBR.gCOffset(-s, -t, 0) + self.legBL.gCOffset(-s, -t, 0))
			time.sleep(sleep2)
			pass


	def _send(self, botcommand):
			print botcommand
			print
			self.sender(botcommand)

