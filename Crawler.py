# -*- coding: latin-1 -*-

import legIK
import time
import math
import json
import sys

MY_DRIVE_SPEED_MIN = 500
MY_DRIVE_SPEED_MAX = 2500

#The class is based on a work by Rob Cook.
# Please visit www.robcook.eu for more details on algorithm and calculations behind it.


class LegEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, legIK.Leg):
            return dict(name            = obj.name,
                        id              = obj.id,
                        offset          = obj.legOffset,
                        coxa            = obj.coxaLengh,
                        temur           = obj.temurLengh,
                        tibia           = obj.tibiaLengh,
                        servos          = obj.servos,
                        initial_state   = obj.initial_state,
                        debug           = obj.debug)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class Controller:
    """Tetrym

     legFL   --##--  legFR
               ##
     legBL   --##--  legBR


    """
    def __init__(self, **kwds):
            self.sender = kwds['sender']

            self.PROTOCOLS = ['Custom tetry', 'Compact', 'Pololu', 'MiniSSC']
            self.GAITS = ["tripod", "wave", "ripple"]
            if 'protocol' in kwds.keys():
                self.protocol = self.PROTOCOLS[(kwds['protocol'])]
            else:
                self.protocol = self.PROTOCOLS[0]
            print "Protocol is %s" % self.protocol

            self.inited = False
            if 'settings' in kwds:
                self.settingsFileName = kwds['settings']
                self.loadSettings(self.settingsFileName)
            self.gait = 1

    def dumpSettings(self):
            sfile = open(self.settingsFileName,'w')
            json.dump(dict(legs = self.legs, inverted = self.inverted),
                      sfile, cls=LegEncoder, indent=1, separators=(',', ': '))

    def loadSettings(self, settingsFileName):
            #load legs from json file
            self.settingsFileName = settingsFileName
            self.legs = []
            try:
                print >>sys.stderr, "Loaded settings from file:", self.settingsFileName
                sfile = open(self.settingsFileName,'r')
                jsettings = json.load(sfile)
                self.legs = range(len(jsettings['legs']))
                for j in jsettings['legs']:
                    #print >> sys.stderr, j
                    # nm = j['name']
                    self.legs[j['id']] = (legIK.Leg(name            = j['name'],
                                                   id               = j['id'],
                                                   offset           = j['offset'],
                                                   coxa             = j['coxa'],
                                                   temur            = j['temur'],
                                                   tibia            = j['tibia'],
                                                   servos           = j['servos'],
                                                   initial_state    = j['initial_state'],
                                                   debug            = j['debug']))
                self.inverted = jsettings['inverted']
                sfile.close()
            except ValueError:
                    pass

            #calculate number of servos
            self.servo_number = 0
            for l in self.legs:
                self.servo_number = self.servo_number + len(l.servos)

            self.sender(start=1)



    def initBot(self):
            bc = []
            for leg in self.legs:
                bc += leg.setInitalState()
            self._send(bc)
            self.inited = True

    def moveToCoordinates(self, coord_d):
            command=[]
            print coord_d
            for lc in coord_d.keys():
                print coord_d[lc][0], coord_d[lc][1], coord_d[lc][2]
                command += self.legs[lc].gCExactCoordinates(coord_d[lc][0], coord_d[lc][1], coord_d[lc][2])
            self._send(command)



    def makeStep(self, angle):
        #TODO: add gaits
        #TODO: select closest leg to direction to start with
            if not self.inited:
                self.initBot()

            d=10
            sleep1=0.1
            sleep2=0.5

            angle = math.radians(angle)
            s,t = math.sin(angle)*d, math.cos(angle)*d
            print "Offsets are: %f, %f" % (s,t)

            if self.GAITS[self.gait] == "wave":
                for leg in self._sortLegsAngle(angle):
                    #assume to start from BasePose
                    #raise each of legs , move forward by 4*d mm, lower it, then move body forward by d mm
                    print leg.id
                    self._legTranspose(leg, s, t, d, sleep1)
                    self._shiftBody(-s, -t)
                    time.sleep(sleep2)
            elif self.GAITS[self.gait] == "ripple":
                pass
            else:
                pass


            pass

    def _sortLegsAngle(self, angle):
        legs_angles = [abs(math.degrees(x.legOffsetAngle-angle)) for x in self.legs]
        min_angle = min(legs_angles)
        closest_legs = [i for i,j in enumerate(legs_angles) if j==min_angle]
        return self.legs[closest_legs[0]:] + self.legs[:closest_legs[0]]

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

            self.sender(message = message, botcommand = botcommand)

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
                        a['position'] = int(round(
                            self._interpolate(a['angle'], 180, -180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX)
                        ))
                    else:
                        a['position'] = int(round(
                            self._interpolate(a['angle'], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX)
                        ))
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
