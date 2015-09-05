# -*- coding: latin-1 -*-

# import legIK
# import time
import math
import traceback
import json
# import sys
import numpy
from TetryTools import MathTools
from twisted.internet import reactor, defer

MY_DRIVE_SPEED_MIN = 500
MY_DRIVE_SPEED_MAX = 2500

# The class is based on a work by Rob Cook.
# Please visit www.robcook.eu for more details on algorithm and calculations behind it.


# class LegEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, legIK.Leg):
#             return dict(name=obj.name,
#                         id=obj.id,
#                         offset=obj.leg_offset,
#                         coxa=obj.coxa_length,
#                         temur=obj.temur_length,
#                         tibia=obj.tibia_length,
#                         servos=obj.servos,
#                         initial_state=obj.initial_state,
#                         debug=obj.debug)
#         # Let the base class default method raise the TypeError
#         return json.JSONEncoder.default(self, obj)


class Controller:
    """Tetry

     legFL   --##--  legFR
               ##
     legBL   --##--  legBR


    """

    # to re-write
    def __init__(self, **kwds):
        self.logger = kwds['logger']
        self.sender = kwds['sender']
        self.app = kwds['app']

        self.protocols = ['Custom tetry', 'Compact', 'Pololu', 'MiniSSC']
        if 'current_protocol' in kwds.keys():
            self.current_protocol = self.protocols[(kwds['current_protocol'])]
        else:
            self.current_protocol = self.protocols[0]
        self.logger(1, "Protocol is %s" % self.current_protocol)

        self.gaits = ["tripod", "wave", "ripple"]
        self.inited = False
        if 'settings' in kwds:
            self.settings_file_name = kwds['settings']
            self.load_settings(self.settings_file_name)
        self.gait = 1
        self.debug = 1
        self.legs = []
        self.inverted = []
        self.servo_number = 0

    # to re-write
    # def dump_settings(self):
    #     sfile = open(self.settings_file_name, 'w')
    #     json.dump(dict(legs=self.legs, inverted=self.inverted),
    #               sfile, cls=LegEncoder, indent=1, separators=(',', ': '))

    # DEPRECATED!
    # @defer.inlineCallbacks
    # def load_settings_from_file(self, settings_file_name):
    #     # load legs from json file
    #     self.settings_file_name = settings_file_name
    #     self.legs = []
    #     try:
    #         self.logger(1, "Loaded settings from file:", self.settings_file_name)
    #         sfile = open(self.settings_file_name, 'r')
    #         jsettings = json.load(sfile)
    #         self.load_settings(jsettings)
    #         sfile.close()
    #     except ValueError:
    #         pass
    #     # yield 1
    #
    #     # calculate number of servos
    #     for l in self.legs:
    #         self.servo_number += len(l.servos)
    #
    #     self.sender(start=1)

    #  OK
    @defer.inlineCallbacks
    def load_settings(self, model):
        self.legs = []
        print len(model[u'legs'])
        for j in model[u'legs']:
            self.legs.append(j['id'])
            print j['name'], j
            try:
                yield self.app.call("com.tetry.{}.init".format(j['id']), j)
            except:
                traceback.print_exc()
            # TODO: legIK should be crossbar.io RPC (service)
        self.inverted = model['inverted']

    # OK
    @defer.inlineCallbacks
    def init_bot(self, *args):
        bc = []
        for leg in self.legs:
            res = yield self.app.call("com.tetry.{}.get_starting_point".format(leg))
            print res
            bc += res
        self._send(bc)
        self.inited = True
        self.logger(1, "Bot inited.")

    # def move_to_coordinates(self, coord_d):
    #     command = []
    #     self.logger(1, coord_d)
    #     for lc in range(len(coord_d)):
    #         self.logger(1, coord_d[lc][0], coord_d[lc][1], coord_d[lc][2])
    #         command += self.legs[lc].go_exact_coordinates(coord_d[lc][0], coord_d[lc][1], coord_d[lc][2])
    #     self._send(command)

    # to re-write
    @defer.inlineCallbacks
    def make_step(self, angle, distance=10):
        # TODO: add gaits
        if not self.inited:
            self.logger(1, "Bot is not initiated yet. Initiating...")
            self.init_bot()

        self.logger(1, "Making step...")
        sleep1 = 0.1
        sleep2 = 0.5

        self.logger(1, angle)
        angle = math.radians(angle)
        s, t = math.sin(angle) * distance, math.cos(angle) * distance
        self.logger(1, "Offsets are: %f, %f" % (s, t))

        if self.gaits[self.gait] == "wave":
            for leg in self._sort_legs_angle(angle):
                # assume to start from BasePose
                # raise each of legs , move forward by 4*d mm, lower it, then move body forward by d mm
                self.logger(1, "Transposing leg: {}".format(leg))
                self._leg_transpose(leg, s, t, distance, sleep1)
                self.shift_body_offset(-s, -t)
                d = defer.Deferred()
                reactor.callLater(sleep2, d.callback, None)
                yield d

        elif self.gaits[self.gait] == "ripple":
            pass
        else:
            pass
        pass

    # to re-write
    def _sort_legs_angle(self, angle):
        """Select closest to direction leg to start with"""
        # TODO: rewrite to return list of strings
        # legs_angles = [abs(math.degrees(x.leg_offset_angle - angle)) for x in self.legs]
        # min_angle = min(legs_angles)
        # closest_legs = [i for i, j in enumerate(legs_angles) if j == min_angle]
        # return self.legs[closest_legs[0]:] + self.legs[:closest_legs[0]]
        return self.legs

    # OK
    def _send(self, bot_command):
        self.logger(1, bot_command)

        bot_command = self._angles2positions(bot_command)

        self.sender(message=self._translate(bot_command), bot_command=bot_command)

    # OK
    def _translate(self, bot_command):
        message = ''

        if self.current_protocol == 'Custom tetry':
            for x in bot_command:
                message += '#%iP%i' % (x['servo'], x['position'])
                # self.sliders[x['servo']].SetValue(x['position'])
            # message = message[::-1]
            message += '\n'

        elif self.current_protocol == 'Compact':
            if len(bot_command) > 1:
                # Set Multiple Targets
                # Compact current_protocol:
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
            self.logger(1, "MiniSSC current_protocol has not been implemented yet!")

        else:
            self.logger(1, "No current_protocol defined!")
        return message

    # OK
    @defer.inlineCallbacks
    def _leg_transpose(self, leg, x_offset, y_offset, depth, sleep_time1):
        # TODO: leg here should be a string referring to required leg
        # TODO: re-write in Twisted way
        rpc = "com.tetry.{}.get_to_offset".format(leg)

        res1 = yield self.app.call(rpc, x_offset, y_offset, -depth)
        self._send(res1)
        d1 = defer.Deferred()
        reactor.callLater(sleep_time1, d1.callback, None)
        yield d1

        res2 = yield self.app.call(rpc, x_offset * 2, y_offset * 2, 0)
        self._send(res2)
        d2 = defer.Deferred()
        reactor.callLater(sleep_time1, d2.callback, None)
        yield d2

        res3 = yield self.app.call(rpc, x_offset, y_offset, depth)
        self._send(res3)
        # d3 = defer.Deferred()
        # reactor.callLater(sleep_time1, d3.callback, None)
        # yield d3

    # OK
    def shift_body_offset(self, x_offset, y_offset):
        ds=[]
        for l in self.legs:
            d = defer.Deferred()
            d.addCallback(self.app.call, "com.tetry.{}.get_to_offset".format(l), x_offset, y_offset, 0)
            ds.append(d)
        dlist = defer.gatherResults(ds, consumeErrors=True)
        dlist.addCallback(self._flatten_list)
        dlist.addCallback(self._send)
        for d in ds:
            reactor.callLater(0, d.callback, None)
            yield d
        # clist = []
        # for leg in self.legs:
        #     rpc = "com.tetry.{}.get_to_offset".format(leg)
        #
        #     clist.extend(l.go_offset(x_offset, y_offset, 0))
        # self._send(clist)
        # pass

    # OK
    def _flatten_list(self, list):
        return [item for sublist in list for item in sublist]

    # OK
    @defer.inlineCallbacks
    def shift_body_angle(self, angle, length=30):
        # TODO: length should be taken from PhysicalModel
        x_offset, y_offset = length * math.cos(math.radians(angle)), length * math.sin(math.radians(angle))
        # clist = []
        ds=[]
        for l in self.legs:
            d = defer.Deferred()
            d.addCallback(self.app.call, "com.tetry.{}.get_to_offset_from_initial".format(l), x_offset, y_offset, 0)
            ds.append(d)
        dlist = defer.gatherResults(ds, consumeErrors=True)
        dlist.addCallback(self._flatten_list)
        dlist.addCallback(self._send)
        for d in ds:
            reactor.callLater(0, d.callback, None)
            yield d


        # clist.extend(l.go_offset_from_initial(x_offset, y_offset, 0))
        # self._send(clist)

    # OK
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

    # OK
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
        ds=[]
        for l in self.legs:
            d = defer.Deferred()
            d.addCallback(self.app.call, "com.tetry.{}.get_rotate".format(l), rotation_matrix)
            ds.append(d)
        dlist = defer.gatherResults(ds, consumeErrors=True)
        dlist.addCallback(self._flatten_list)
        dlist.addCallback(self._send)
        for d in ds:
            reactor.callWhenRunning(d.callback)
            yield d

        # bot_command = []
        # for l in self.legs:
        #     bot_command.extend(l.rotate(rotation_matrix))
        # self._send(bot_command)

    # OK
    @defer.inlineCallbacks
    def sleep(self, duration=1.0):
        d = defer.Deferred()
        reactor.callLater(duration, d.callback, duration)
        yield d
