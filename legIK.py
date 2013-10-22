import math

MY_DRIVE_SPEED_MIN = 500
MY_DRIVE_SPEED_MAX = 2500

class legIK:
    """ new legIK(offset=[-65.8, 76.3], angle=-2.2829, coxa=29.0, temur=49, tibia=52)  docstring for legIK"""
    def __init__(self, *args, **kwds):
        #super(legIK, self).__init__()
        self.legOffset = kwds['offset']
        self.legOffsetAngle = math.atan2(self.legOffset[1], self.legOffset[0])
        print "legOffsetAngle=", math.degrees(self.legOffsetAngle)
        self.coxaLengh = kwds['coxa']
        self.temurLengh = kwds['temur']
        self.tibiaLengh = kwds['tibia']
        self.servos = kwds['servos']

    def _ikLowerLeg(self, x, y):
        #print "IK function called. x=", x, "y=", y
        print "Lower leg targets are:", x, y
        try:
            d = math.sqrt(x**2+y**2)
            k = (d**2-self.tibiaLengh**2+self.temurLengh**2)/(2*d)
            m = math.sqrt(self.temurLengh**2-k*k)
        except ZeroDivisionError:
            print "Divide by Zero error. No valid joint solution."
            return
        except ValueError:
            print "Math function error. Probably square root of negative number. No valid joint solution."
            return
        theta = math.degrees(math.atan2(float(y),float(x))-math.atan2(m,k))
        phi   = math.degrees(math.atan2(m,k)+math.atan2(m,(d-k)))
        returnAngles = [theta, phi]
        #print "theta=", theta, "phi=", phi
        return returnAngles        
        
    def _ikFullLeg(self, x, y, z):
        alpha = math.degrees(math.atan2(y, x))
        lowerLegAngles = self._ikLowerLeg(math.sqrt(x**2+y**2) - self.coxaLengh, z)
        if (lowerLegAngles == None):
            print "No ikFullLeg calculation available!"
            return 
        else:
            print "ikFullLeg ", round(alpha), round(lowerLegAngles[0]), round(lowerLegAngles[1])
            returnAngles = [alpha, lowerLegAngles[0], lowerLegAngles[1]] 
            return returnAngles

    def getAngles(self,x,y,z):
        x = x - self.legOffset[0]
        y = y - self.legOffset[1]
        # rotate to leg zero position
        print "Leg local targets in global coordinates are x=", x, " y=", y, "z=", z
        legx=math.cos(self.legOffsetAngle)*x - math.sin(self.legOffsetAngle)*y
        legy=math.sin(self.legOffsetAngle)*x + math.cos(self.legOffsetAngle)*y
        # get IK solution and move leg
        print "Leg targets in local coordinates are legX=%.2f" % legx, " legY=%.2f" % legy, z
        s = self._ikFullLeg(legx,legy,z)
        if (s==None):
            print "No angles available!"
            return [0, 0, 0]
        else:
            #print "%.2f" % s[0], "%.2f" % s[1], "%.2f" % s[2]
            return s

    def _interpolate (self, x, minS, maxS, minD, maxD):
        try:
            x = (maxD-minD)*(x-minS)/(maxS-minS)+minD
        except ZeroDivisionError:
            print "Divide by Zero error. "
            return
        except ValueError:
            print "Math function error."
            return
        return x

    def getPositions (self, x, y, z):
        print "Global targets are:", x, y, z
        some = self.getAngles(x, y, z)
        some[0] = round(self._interpolate(some[0], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX))
        some[1] = round(self._interpolate(some[1], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX))
        some[2] = round(self._interpolate(some[2], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX))
        print "Positions:", some
        return some

    def getCommand(self,x,y,z):
        [xp,yp,zp] = self.getPositions(x,y,z)
        command =  '#' + str(self.servos[0]) + 'P' + str(xp)
        command =+ '#' + str(self.servos[1]) + 'P' + str(yp)
        command =+ '#' + str(self.servos[2]) + 'P' + str(zp)
        return command


