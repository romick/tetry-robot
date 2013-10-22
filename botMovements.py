import legIK

class Tetry():
	"""docstring for Tetrym"""
	def __init__(self, *arg, **kwarg):
		#super(Tetrye self).__init__()
        legFR = legIK(offset=[25,25],   coxa=45, temur=45, tibia=85, servos=[0,1,2])
        legFL = legIK(offset=[-25,25],  coxa=45, temur=45, tibia=85, servos=[3,4,5])
        legBR = legIK(offset=[25,-25],  coxa=45, temur=45, tibia=85, servos=[6,7,8])
        legBL = legIK(offset=[-25,-25], coxa=45, temur=45, tibia=85, servos=[9,10,11])
		self.arg = arg

	def makeStepForward(self):
		pass

	def makeBasePose(self):
		return legFR.getCommand(75,75,40) + legFL.getCommand(-75,75,40) + legBR.getCommand(75,-75,40) + legBL.getCommand(-75,-75,40)
		pass