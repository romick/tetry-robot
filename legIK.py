import math
import sys


class Leg:
    """ new legIK(offset=[-65.8, 76.3], angle=-2.2829, coxa=29.0, temur=49, tibia=52)  docstring for legIK"""
    def __init__(self, *args, **kwds):
        self.legOffset = kwds['offset']
        self.coxaLengh = kwds['coxa']
        self.temurLengh = kwds['temur']
        self.tibiaLengh = kwds['tibia']
        self.servos = kwds['servos']
        self.name = kwds['name']
        self.stateX = 0
        self.stateY = 0
        self.stateZ = 0
        if 'debug' in kwds.keys():
            self.debug = kwds['debug']
        else:
            self.debug = False

        
        self.legOffsetAngle = math.atan2(self.legOffset[0], self.legOffset[1])
        if self.legOffsetAngle < 0:
            self.legOffsetAngle = 2*math.pi + self.legOffsetAngle
        if self.debug:
            print self.name, ": legOffsetAngle(radians)=", self.legOffsetAngle
            print self.name, ": legOffsetAngle(degrees)=", math.degrees(self.legOffsetAngle)



    def _ikLowerLeg(self, x, y):
        #print "IK function called. x=", x, "y=", y
        if self.debug:
            print "Lower leg targets are:", x, y
        try:
            d = math.sqrt(x**2+y**2)
            k = (d**2-self.tibiaLengh**2+self.temurLengh**2)/(2*d)
            m = math.sqrt(self.temurLengh**2-k*k)
        except ZeroDivisionError:
            if self.debug:
                print "Divide by Zero error. No valid joint solution."
            return
        except ValueError:
            if self.debug:
                print "Math function error. Probably square root of negative number. No valid joint solution."
            return
        theta = math.degrees(math.atan2(float(y),float(x))-math.atan2(m,k))
        phi   = math.degrees(math.atan2(m,k)+math.atan2(m,(d-k)))
        returnAngles = [theta, phi]
        #print "theta=", theta, "phi=", phi
        return returnAngles        
        
    def _ikFullLeg(self, x, y, z):
        alpha = math.degrees(math.atan2(x, y))
        # if alpha < 0:
            # alpha = 360 + alpha
        lowerLegAngles = self._ikLowerLeg(math.sqrt(x**2+y**2) - self.coxaLengh, z)
        if (lowerLegAngles == None):
            if self.debug:
                print "No ikFullLeg calculation available!"
            return 
        else:
            if self.debug:
                print "ikFullLeg ", round(alpha), round(lowerLegAngles[0]), round(lowerLegAngles[1])
            returnAngles = [alpha, lowerLegAngles[0], lowerLegAngles[1]] 
            return returnAngles

    def _getAngles(self,x,y,z):
        if self.debug:
            print
            print self.name, ": Global targets are:", x, y, z
        #re-calculate position
        cosa = math.cos(self.legOffsetAngle)
        sina = math.sin(self.legOffsetAngle)

        x = math.copysign((x - self.legOffset[0]), sina)
        y = math.copysign((y - self.legOffset[1]), cosa)
        # rotate to leg zero position
        if self.debug:
            print "Cosa", cosa, "Sina",  sina
            print "Leg local targets in global coordinates are x=", x, " y=", y, "z=", z
        legx=cosa*x - sina*y
        legy=sina*x + cosa*y
        # get IK solution and move leg
        if self.debug:
            print "Leg targets in local coordinates are legX=%.2f" % legx, " legY=%.2f" % legy, z
        s = self._ikFullLeg(legx,legy,z)
        if (s==None):
            if self.debug:
                print "No angles available!"
            return [0, 0, 0]
        else:
            #print "%.2f" % s[0], "%.2f" % s[1], "%.2f" % s[2]
            return s


    #def _getPositions (self, x, y, z):
    #    some = self._getAngles(x, y, z)
    #    some[0] = round(self._interpolate(some[0], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX))
    #    some[1] = round(self._interpolate(some[1], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX))
    #    some[2] = round(self._interpolate(some[2], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX))
    #    if self.debug:
    #        print "Positions:", some
    #    return some

    def gCExactCoordinates(self,x,y,z):
        #TODO: move state storage to separate class (is it really needed?)

        #check if targets set
        if x is None: x = self.stateX 
        if y is None: y = self.stateY 
        if z is None: z = self.stateZ 

        #save current position
        self.stateX = int(x)
        self.stateY = int(y)
        self.stateZ = int(z)
        #print >> sys.stderr, self.stateX, self.stateY, self.stateZ
        
        [xp,yp,zp] = self._getAngles(x,y,z)
        commandlist =  []
        commandlist.append(dict(servo=self.servos[0], angle=int(xp)))
        commandlist.append(dict(servo=self.servos[1], angle=int(yp)))
        commandlist.append(dict(servo=self.servos[2], angle=int(zp)))
        return commandlist

    def gCOffset(self, xOffset, yOffset, zOffset):
        return self.gCExactCoordinates(self.stateX + xOffset, self.stateY + yOffset, self.stateZ + zOffset)
