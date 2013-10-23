
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
		self.legFR.getCommandOffsetCoordinates(5,  0, -10)
		self.legFR.getCommandOffsetCoordinates(10, 0, 0)
		self.legFR.getCommandOffsetCoordinates(5,  0, 10)

		#move body forward by 5mm
		self.legFR.getCommandOffsetCoordinates(-5,0,0)
		self.legFL.getCommandOffsetCoordinates(-5,0,0)
		self.legBR.getCommandOffsetCoordinates(-5,0,0)
		self.legBL.getCommandOffsetCoordinates(-5,0,0)

		#raise Back Left leg , move forward by 20mm, lower it
		self.legBL.getCommandOffsetCoordinates(5,  0, -10)
		self.legBL.getCommandOffsetCoordinates(10, 0, 0)
		self.legBL.getCommandOffsetCoordinates(5,  0, 10)

		#move body forward by 5mm
		self.legFR.getCommandOffsetCoordinates(-5,0,0)
		self.legFL.getCommandOffsetCoordinates(-5,0,0)
		self.legBR.getCommandOffsetCoordinates(-5,0,0)
		self.legBL.getCommandOffsetCoordinates(-5,0,0)

		#raise Front Left leg , move forward by 20mm, lower it
		self.legFL.getCommandOffsetCoordinates(5,  0, -10)
		self.legFL.getCommandOffsetCoordinates(10, 0, 0)
		self.legFL.getCommandOffsetCoordinates(5,  0, 10)

		#move body forward by 5mm
		self.legFR.getCommandOffsetCoordinates(-5,0,0)
		self.legFL.getCommandOffsetCoordinates(-5,0,0)
		self.legBR.getCommandOffsetCoordinates(-5,0,0)
		self.legBL.getCommandOffsetCoordinates(-5,0,0)

		#raise Back Right leg , move forward by 20mm, lower it
		self.legBR.getCommandOffsetCoordinates(5,  0, -10)
		self.legBR.getCommandOffsetCoordinates(10, 0, 0)
		self.legBR.getCommandOffsetCoordinates(5,  0, 10)

		#move body forward by 5mm
		self.legFR.getCommandOffsetCoordinates(-5,0,0)
		self.legFL.getCommandOffsetCoordinates(-5,0,0)
		self.legBR.getCommandOffsetCoordinates(-5,0,0)
		self.legBL.getCommandOffsetCoordinates(-5,0,0)
		pass

	def makeBasePose(self):
		return self.legFR.getCommand(75,75,40) + self.legFL.getCommand(-75,75,40) + self.legBR.getCommand(75,-75,40) + self.legBL.getCommand(-75,-75,40)
