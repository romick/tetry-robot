# -*- coding: latin-1 -*-

import legIK
import time
import math

MY_DRIVE_SPEED_MIN = 500
MY_DRIVE_SPEED_MAX = 2500

#The class is based on a work by Rob Cook.
# Please visit www.robcook.eu for more details on algorithm and calculations behind it.

class Robot:
    """Tetrym

     legFL   --##--  legFR
               ##
     legBL   --##--  legBR


    """
    def __init__(self, **kwds):
            self.protocol_list = ['Custom tetry', 'Compact', 'Pololu', 'MiniSSC']
            self.legs = []
            self.legs.append(legIK.leg(offset=[25,25],   coxa=45, temur=45, tibia=85, servos=[0,1,2],   name="FR leg", debug=False))
            self.legs.append(legIK.leg(offset=[-25,25],  coxa=45, temur=45, tibia=85, servos=[3,4,5],   name="FL leg", debug=False))
            self.legs.append(legIK.leg(offset=[25,-25],  coxa=45, temur=45, tibia=85, servos=[6,7,8],   name="BR leg", debug=False))
            self.legs.append(legIK.leg(offset=[-25,-25], coxa=45, temur=45, tibia=85, servos=[9,10,11], name="BL leg", debug=False))
            for l in self.legs:
                print l.name
            self.servo_number = 12
            self.sender = kwds['sender']
            self.inverted = [2,5,8,11]

            if 'protocol' in kwds.keys():
                self.protocol = self.protocol_list[(kwds['protocol'])]
            else:
                self.protocol = self.protocol_list[0]
            print "Protocol is %s" % self.protocol

            self.inited = False

            # self.initBot()

    def initBot(self):
            a = 65
            b = 65
            c = 60
            self._send(self.legs[0].gCExactCoordinates(a, b, c) +
                       self.legs[1].gCExactCoordinates(-a, b, c)+
                       self.legs[2].gCExactCoordinates(a, -b, c)+
                       self.legs[3].gCExactCoordinates(-a, -b, c))

    def makeStep(self, angle):
            if not self.inited:
                self.initBot()

            d=10
            sleep1=0.1
            sleep2=0.5

            angle = math.radians(angle)
            s,t = math.sin(angle)*d, math.cos(angle)*d
            print "Offsets are: %f, %f" % (s,t)

            for leg in self.legs:
                #assume to start from BasePose
                #raise each of legs , move forward by 4*d mm, lower it, then move body forward by d mm
                self._legTranspose(leg, s, t, d, sleep1)
                self._shiftBody(-s, -t)
                time.sleep(sleep2)

            pass


    def _send(self, botcommand):
            print botcommand
            print

            message = ''

            botcommand = self._angles2positions(botcommand)

            if self.protocol == 'Custom tetry':
                for x in botcommand: 
                    message = message + '#%iP%i' % (x['servo'], x['position'])
                    # self.sliders[x['servo']].SetValue(x['position'])
                #message = message[::-1]
                message = message  + '\n'

            elif self.protocol == 'Compact':
                if len(botcommand) > 1:
                    #Set Multiple Targets
                    #Compact protocol:
                    # 0x9F,
                    # number of targets,
                    # first channel number,
                    # first target low bits,
                    # first target high bits,
                    # second target low bits,
                    # second target high bits,
                    # …
                    message = chr(0x9F) + chr(len(botcommand))
                    for x in botcommand: 
                        posi = x['position'] * 4
                        message = message + \
                                  chr(x['servo']) + \
                                  chr(posi & 0x7F) + \
                                  chr((posi >> 7) & 0x7F)
                else:
                    posi = botcommand[0]['position'] * 4
                    message = chr(84) + \
                              chr(botcommand[0]['servo']) + \
                              chr(posi & 0x7F) + \
                              chr((posi >> 7) & 0x7F)

            elif self.protocol == 'Pololu':
                pololu_device_number = 12
                if len(botcommand) > 1:
                    #Set Multiple Targets
                    #Pololu protocol:
                    # 0xAA,
                    # device number,
                    # 0x1F,
                    # number of targets,
                    # first channel number,
                    # first target low bits,
                    # first target high bits,
                    # second target low bits,
                    # second target high bits,
                    # …
                    message = chr(0xAA) + chr(pololu_device_number) + chr(0x1F) + chr(len(botcommand))
                    for x in botcommand: 
                        posi = x['position'] * 4
                        message = message + \
                                  chr(x['servo']) + \
                                  chr(posi & 0x7F) + \
                                  chr((posi >> 7) & 0x7F)
                else:
                    posi = botcommand[0]['position'] * 4
                    message = chr(0xAA) + \
                              chr(pololu_device_number) + \
                              chr(4) + \
                              chr(botcommand[0]['servo']) + \
                              chr(posi & 0x7F) + \
                              chr((posi >> 7) & 0x7F)
                
            elif self.protocol == 'MiniSSC':
                print "MiniSSC protocol has not been implemented yet!"

            else:
                print "No protocol defined!"

            self.sender(message)

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
            for l in self.legs:
                clist.extend(l.gCOffset(xOffset, yOffset, 0))
            self._send(clist)
            pass

    def _angles2positions (self, alist):
            plist = []
            for a in alist:
                if 'position' not in a.keys():
                    if a['servo'] in self.inverted:
                        a['position'] = int(round(self._interpolate(a['angle'], 180, -180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX)))
                    else:
                        a['position'] = int(round(self._interpolate(a['angle'], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX)))
                plist.append(a)
            return plist




    def _interpolate (self, x, minS, maxS, minD, maxD):
        try:
            x = (maxD-minD)*(x-minS)/(maxS-minS)+minD
        except ZeroDivisionError:
            if self.debug:
                print "Divide by Zero error. "
            return
        except ValueError:
            if self.debug:
                print "Math function error."
            return
        return x
