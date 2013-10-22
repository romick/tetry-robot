#TODO: make a separate class for bot positions storage

import legIK

class Tetry():
	"""docstring for Tetrym"""
	def __init__(self, *arg, **kwarg):
		#super(Tetrye self).__init__()
        self.legFR = legIK(offset=[25,25],   coxa=45, temur=45, tibia=85, servos=[0,1,2])
        self.legFL = legIK(offset=[-25,25],  coxa=45, temur=45, tibia=85, servos=[3,4,5])
        self.legBR = legIK(offset=[25,-25],  coxa=45, temur=45, tibia=85, servos=[6,7,8])
        self.legBL = legIK(offset=[-25,-25], coxa=45, temur=45, tibia=85, servos=[9,10,11])

	def makeStepForward(self):
		#TODO: it is just order of commands - make it a program
		
		#assume to start from BasePose
		#raise Front Right leg , move forward by 20mm, lower it
		self.legFR.getCommand(80,75,30)
		self.legFR.getCommand(90,75,30)
		self.legFR.getCommand(95,75,40)

		#move body forward by 5mm
		self.legFR.getCommand(90,75,40)
		self.legFL.getCommand(-80,75,40)
		self.legBR.getCommand(70,-75,40)
		self.legBL.getCommand(-80,-75,40)

		#raise Back Left leg , move forward by 20mm, lower it
		self.legBL.getCommand(-75,-75,30)
		self.legBL.getCommand(-65,-75,30)
		self.legBL.getCommand(-60,-75,40)

		#move body forward by 5mm
		self.legFR.getCommand(85,75,40)
		self.legFL.getCommand(-85,75,40)
		self.legBR.getCommand(65,-75,40)
		self.legBL.getCommand(-65,-75,40)

		pass

	def makeBasePose(self):
		return self.legFR.getCommand(75,75,40) + self.legFL.getCommand(-75,75,40) + self.legBR.getCommand(75,-75,40) + self.legBL.getCommand(-75,-75,40)
