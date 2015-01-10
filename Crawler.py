# -*- coding: latin-1 -*-

import legIK
import time
import math
import json
import sys
import numpy
from TetryTools import MathTools

MY_DRIVE_SPEED_MIN = 500
MY_DRIVE_SPEED_MAX = 2500

#The class is based on a work by Rob Cook.
# Please visit www.robcook.eu for more details on algorithm and calculations behind it.


class LegEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, legIK.Leg):
            return dict(name=obj.name,
                        id=obj.id,
                        offset=obj.leg_offset,
                        coxa=obj.coxa_length,
                        temur=obj.temur_length,
                        tibia=obj.tibia_length,
                        servos=obj.servos,
                        initial_state=obj.initial_state,
                        debug=obj.debug)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class Controller:
    """Tetry

     legFL   --##--  legFR
               ##
     legBL   --##--  legBR


    """

    def __init__(self, **kwds):
        self.sender = kwds['sender']

        self.protocols = ['Custom tetry', 'Compact', 'Pololu', 'MiniSSC']
        self.gaits = ["tripod", "wave", "ripple"]
        if 'current_protocol' in kwds.keys():
            self.current_protocol = self.protocols[(kwds['current_protocol'])]
        else:
            self.current_protocol = self.protocols[0]
        print "Protocol is %s" % self.current_protocol

        self.inited = False
        if 'settings' in kwds:
            self.settings_file_name = kwds['settings']
            self.load_settings(self.settings_file_name)
        self.gait = 1
        self.debug = 1
        self.legs = []
        self.inverted = []
        self.servo_number = 0

    def dump_settings(self):
        sfile = open(self.settings_file_name, 'w')
        json.dump(dict(legs=self.legs, inverted=self.inverted),
                  sfile, cls=LegEncoder, indent=1, separators=(',', ': '))

    def load_settings(self, settings_file_name):
        #load legs from json file
        self.settings_file_name = settings_file_name
        self.legs = []
        try:
            print >> sys.stderr, "Loaded settings from file:", self.settings_file_name
            sfile = open(self.settings_file_name, 'r')
            jsettings = json.load(sfile)
            self.legs = range(len(jsettings['legs']))
            for j in jsettings['legs']:
                #print >> sys.stderr, j
                # nm = j['name']
                self.legs[j['id']] = (legIK.Leg(name=j['name'],
                                                id=j['id'],
                                                offset=j['offset'],
                                                coxa=j['coxa'],
                                                temur=j['temur'],
                                                tibia=j['tibia'],
                                                servos=j['servos'],
                                                initial_state=j['initial_state'],
                                                debug=j['debug']))
            self.inverted = jsettings['inverted']
            sfile.close()
        except ValueError:
            pass

        #calculate number of servos
        for l in self.legs:
            self.servo_number += len(l.servos)

        self.sender(start=1)

    def init_bot(self):
        bc = []
        for leg in self.legs:
            bc += leg.set_initial_state()
        self._send(bc)
        self.inited = True

    def move_to_coordinates(self, coord_d):
        command = []
        print coord_d
        for lc in range(len(coord_d)):
            print coord_d[lc][0], coord_d[lc][1], coord_d[lc][2]
            command += self.legs[lc].go_exact_coordinates(coord_d[lc][0], coord_d[lc][1], coord_d[lc][2])
        self._send(command)

    def make_step(self, angle, distance=10):
        #TODO: add gaits
        if not self.inited:
            self.init_bot()

        sleep1 = 0.1
        sleep2 = 0.5

        print angle
        angle = math.radians(angle)
        s, t = math.sin(angle) * distance, math.cos(angle) * distance
        print "Offsets are: %f, %f" % (s, t)

        if self.gaits[self.gait] == "wave":
            for leg in self._sort_legs_angle(angle):
                #assume to start from BasePose
                #raise each of legs , move forward by 4*d mm, lower it, then move body forward by d mm
                print leg.id
                self._leg_transpose(leg, s, t, distance, sleep1)
                self.shift_body_offset(-s, -t)
                time.sleep(sleep2)
        elif self.gaits[self.gait] == "ripple":
            pass
        else:
            pass
        pass

    def _sort_legs_angle(self, angle):
        """Select closest to direction leg to start with"""
        legs_angles = [abs(math.degrees(x.leg_offset_angle - angle)) for x in self.legs]
        min_angle = min(legs_angles)
        closest_legs = [i for i, j in enumerate(legs_angles) if j == min_angle]
        return self.legs[closest_legs[0]:] + self.legs[:closest_legs[0]]

    def _send(self, bot_command):
        print bot_command
        print

        message = ''

        bot_command = self._angles2positions(bot_command)

        if self.current_protocol == 'Custom tetry':
            for x in bot_command:
                message += '#%iP%i' % (x['servo'], x['position'])
                # self.sliders[x['servo']].SetValue(x['position'])
            #message = message[::-1]
            message += '\n'

        elif self.current_protocol == 'Compact':
            if len(bot_command) > 1:
                #Set Multiple Targets
                #Compact current_protocol:
                # 0x9F,
                # number of targets,
                # first channel number,
                # first target low bits,
                # first target high bits,
                # second target low bits,
                # second target high bits,
                # …
                message = chr(0x9F) + chr(len(bot_command))
                for x in bot_command:
                    posi = x['position'] * 4
                    message = message + \
                              chr(x['servo']) + \
                              chr(posi & 0x7F) + \
                              chr((posi >> 7) & 0x7F)
            else:
                posi = bot_command[0]['position'] * 4
                message = chr(84) + \
                          chr(bot_command[0]['servo']) + \
                          chr(posi & 0x7F) + \
                          chr((posi >> 7) & 0x7F)

        elif self.current_protocol == 'Pololu':
            pololu_device_number = 12
            if len(bot_command) > 1:
                #Set Multiple Targets
                #Pololu current_protocol:
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
                message = chr(0xAA) + chr(pololu_device_number) + chr(0x1F) + chr(len(bot_command))
                for x in bot_command:
                    posi = x['position'] * 4
                    message = message + \
                              chr(x['servo']) + \
                              chr(posi & 0x7F) + \
                              chr((posi >> 7) & 0x7F)
            else:
                posi = bot_command[0]['position'] * 4
                message = chr(0xAA) + \
                          chr(pololu_device_number) + \
                          chr(4) + \
                          chr(bot_command[0]['servo']) + \
                          chr(posi & 0x7F) + \
                          chr((posi >> 7) & 0x7F)

        elif self.current_protocol == 'MiniSSC':
            print "MiniSSC current_protocol has not been implemented yet!"

        else:
            print "No current_protocol defined!"

        self.sender(message=message, bot_command=bot_command)

    def _leg_transpose(self, leg, x_offset, y_offset, depth, sleep_time1):
        self._send(leg.go_offset(x_offset, y_offset, -depth))
        time.sleep(sleep_time1)
        self._send(leg.go_offset(x_offset * 2, y_offset * 2, 0))
        time.sleep(sleep_time1)
        self._send(leg.go_offset(x_offset, y_offset, depth))
        time.sleep(sleep_time1)
        pass

    def shift_body_offset(self, x_offset, y_offset):
        clist = []
        for l in self.legs:
            clist.extend(l.go_offset(x_offset, y_offset, 0))
        self._send(clist)
        # pass

    def shift_body_angle(self, angle, length=30):
        x_offset, y_offset = length * math.cos(math.radians(angle)), length * math.sin(math.radians(angle))
        clist = []
        for l in self.legs:
            clist.extend(l.go_offset_from_initial(x_offset, y_offset, 0))
        self._send(clist)

    def _angles2positions(self, alist):
        plist = []
        for a in alist:
            if 'position' not in a.keys():
                if a['servo'] in self.inverted:
                    a['position'] = int(round(
                        MathTools.interpolate(a['angle'], 180, -180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX)
                    ))
                else:
                    a['position'] = int(round(
                        MathTools.interpolate(a['angle'], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX)
                    ))
            plist.append(a)
        return plist

    def rotate_body(self, angle=0, axis_vector=(0, 0, 0)):
        from math import cos, sin
        angle = math.radians(angle)
        (l, m, n) = MathTools.normalize(*axis_vector)
        rotation_matrix = numpy.array([[l * l * (1 - cos(angle)) + cos(angle),
                                        m * l * (1 - cos(angle)) - n * sin(angle),
                                        n * l * (1 - cos(angle)) + m * sin(angle)],
                                       [l * m * (1 - cos(angle)) + n * sin(angle),
                                        m * m * (1 - cos(angle)) + cos(angle),
                                        n * m * (1 - cos(angle)) - l * sin(angle)],
                                       [l * n * (1 - cos(angle)) - m * sin(angle),
                                        m * n * (1 - cos(angle)) + l * sin(angle),
                                        n * n * (1 - cos(angle)) + cos(angle)]])
        bot_command = []
        for l in self.legs:
            bot_command.extend(l.rotate(rotation_matrix))
        self._send(bot_command)

    def sleep(self, duration=1):
        self.sender(update=1)
        time.sleep(duration)
        self.sender(update=1)