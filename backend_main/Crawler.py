# -*- coding: latin-1 -*-

# import legIK
# import time
import math
import traceback
import numpy
from twisted.internet import reactor, defer
from twisted.internet.defer import inlineCallbacks

# The class is based on a work by Rob Cook.
# Please visit www.robcook.eu for more details on algorithm and calculations behind it.


# @staticmethod
def normalize(*args):
    v_length = vector_length(*args)
    if not v_length == 0:
        return (x / v_length for x in args)
    else:
        return args


# @staticmethod
def vector_length(*args):
    print args
    return math.sqrt(sum(x**2 for x in args))
    # return math.sqrt(args[0]**2 + args[1]**2)


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
        self.gaits = ["tripod", "wave", "ripple"]
        self.inited = False
        # if 'settings' in kwds:
        #     self.settings_file_name = kwds['settings']
        #     self.load_settings(self.settings_file_name)
        self.gait = 1
        self.debug = 1
        self.legs = []
        self.inverted = []
        self.servo_number = 0

    # @defer.inlineCallbacks
    # def load_settings(self, model):
    #     self.legs = []
    #     print len(model[u'legs'])
    #     for j in model[u'legs']:
    #         self.legs.append(j['id'])
    #         print j['name'], j
    #         try:
    #             yield self.app.call("com.tetry.{}.init".format(j['id']), j)
    #         except:
    #             traceback.print_exc()
    #     self.inverted = model['inverted']

    @inlineCallbacks
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
    @inlineCallbacks
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

    @inlineCallbacks
    def _send(self, bot_command):
        self.logger(1, bot_command)
        yield self.app.call("com.tetry.queue.append", bot_command)

    @inlineCallbacks
    def _leg_transpose(self, leg, x_offset, y_offset, depth, sleep_time1):
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

    def shift_body_offset(self, x_offset, y_offset):
        ds = []
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
    @inlineCallbacks
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

    # OK
    def rotate_body(self, angle=0, axis_vector=(0, 0, 0)):
        from math import cos, sin
        angle = math.radians(angle)
        (l, m, n) = normalize(*axis_vector)
        rotation_matrix = numpy.array([[l * l * (1 - cos(angle)) + cos(angle),
                                        m * l * (1 - cos(angle)) - n * sin(angle),
                                        n * l * (1 - cos(angle)) + m * sin(angle)],
                                       [l * m * (1 - cos(angle)) + n * sin(angle),
                                        m * m * (1 - cos(angle)) + cos(angle),
                                        n * m * (1 - cos(angle)) - l * sin(angle)],
                                       [l * n * (1 - cos(angle)) - m * sin(angle),
                                        m * n * (1 - cos(angle)) + l * sin(angle),
                                        n * n * (1 - cos(angle)) + cos(angle)]])
        ds = []
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
