
import legIK
import time
import math

class Robot:
    """Tetrym

     legFL   --##--  legFR
               ##
     legBL   --##--  legBR


    """
    def __init__(self, **kwds):
            self.legFR = legIK.leg(offset=[25,25],   coxa=45, temur=45, tibia=85, servos=[0,1,2])
            self.legFL = legIK.leg(offset=[-25,25],  coxa=45, temur=45, tibia=85, servos=[3,4,5])
            self.legBR = legIK.leg(offset=[25,-25],  coxa=45, temur=45, tibia=85, servos=[6,7,8])
            self.legBL = legIK.leg(offset=[-25,-25], coxa=45, temur=45, tibia=85, servos=[9,10,11])
            self.sender = kwds['sender']

            self.initBot()


    def initBot(self):
            self._send(self.legFR.gCExactCoordinates(95, 95, -40)+self.legFL.gCExactCoordinates(-95, 95, -40)+self.legBR.gCExactCoordinates(95, -95, -40)+self.legBL.gCExactCoordinates(-95, -95, -40))

    def makeStep(self, angle):


            angle = math.radians(angle)

            s,t = math.sin(angle)*5, math.cos(angle)*5

            print "Offsets are: %f, %f" % (s,t)

            d=10
            sleep1=0.1
            sleep2=0.5

            #assume to start from BasePose
            #raise Front Right leg , move forward by 20mm, lower it, then move body forward by 5mm
            self._legTranspose(self.legFR, s, t, d, sleep1)
            self._shiftBody(-s, -t)
            time.sleep(sleep2)

            #raise Back Left leg , move forward by 20mm, lower it, then move body forward by 5mm
            self._legTranspose(self.legBL, s, t, d, sleep1)
            self._shiftBody(-s, -t)
            time.sleep(sleep2)

            #raise Front Left leg , move forward by 20mm, lower it, then move body forward by 5mm
            self._legTranspose(self.legFL, s, t, d, sleep1)
            self._shiftBody(-s, -t)
            time.sleep(sleep2)

            #raise Back Right leg , move forward by 20mm, lower it, then move body forward by 5mm
            self._legTranspose(self.legBR, s, t, d, sleep1)
            self._shiftBody(-s, -t)
            time.sleep(sleep2)
            pass


    def _send(self, botcommand):
            print botcommand
            print
            self.sender(botcommand)

    def _legTranspose (self, leg, xOffset, yOffset, depth, sleeptime1):
            self._send(leg.gCOffset(xOffset,  yOffset, -depth))
            time.sleep(sleeptime1)
            self._send(leg.gCOffset(xOffset*2, yOffset*2, 0))
            time.sleep(sleeptime1)
            self._send(leg.gCOffset(xOffset,  yOffset, depth))
            time.sleep(sleeptime1)
            pass

    def _shiftBody(self, xOffset, yOffset):
            clist = []
            clist.extend(self.legFR.gCOffset(xOffset, yOffset, 0))
            clist.extend(self.legFL.gCOffset(xOffset, yOffset, 0))
            clist.extend(self.legBR.gCOffset(xOffset, yOffset, 0))
            clist.extend(self.legBL.gCOffset(xOffset, yOffset, 0))
            self._send(clist)
            pass
