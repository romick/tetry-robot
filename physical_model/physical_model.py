__author__ = 'romick'

import sys
if sys.platform == 'win32':
    ## on windows, we need to use the following reactor for serial support
    ## http://twistedmatrix.com/trac/ticket/3802
    ##
    from twisted.internet import win32eventreactor

    win32eventreactor.install()

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession



class PhysicalModel(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("MyComponent ready! Configuration: {}".format(self.config.extra))

        self.model = self.config.extra
        yield self.register(self.get, u"com.tetry.get_model")
        print "com.tetry.get_model registered"

    def get(self):
        return self.model

if __name__ == '__main__':
    #

    print("Using Twisted reactor {0}".format(reactor.__class__))
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", u"realm1",
                               extra ={"legs":
                                           {
                                               "FR leg":
                                                    {
                                                        "type": "3joints",
                                                        "temur": 45,
                                                        "name": "FR leg",
                                                        "offset": [25, 25],
                                                        "debug": false,
                                                        "coxa": 85,
                                                        "servos": [0, 1, 2],
                                                        "tibia": 85
                                                    },
                                               "MR leg":
                                                    {
                                                        "type": "3joints",
                                                        "temur": 45,
                                                        "name": "MR leg",
                                                        "offset": [25, 0],
                                                        "debug": false,
                                                        "coxa": 85,
                                                        "servos": [0, 1, 2],
                                                        "tibia": 85
                                                    },
                                               "BR leg":
                                                    {
                                                        "type": "3joints",
                                                        "temur": 45,
                                                        "name": "BR leg",
                                                        "offset": [25, -25],
                                                        "debug": false,
                                                        "coxa": 85,
                                                        "servos": [6, 7, 8],
                                                        "tibia": 85
                                                    },
                                               "FL leg":
                                                   {
                                                       "temur": 45,
                                                       "name": "FL leg",
                                                       "offset": [-25, 25],
                                                       "debug": false,
                                                       "coxa": 85,
                                                       "servos": [3, 4, 5],
                                                       "tibia": 85
                                                   },
                                               "BL leg":
                                                   {
                                                       "temur": 45,
                                                       "name": "BL leg",
                                                       "offset": [-25, -25],
                                                       "debug": false,
                                                       "coxa": 85,
                                                       "servos": [9, 10, 11],
                                                       "tibia": 85},
                                               "ML leg":
                                                   {
                                                       "temur": 45,
                                                       "name": "ML leg",
                                                       "offset": [-25, 0],
                                                       "debug": false,
                                                       "coxa": 85,
                                                       "servos": [3, 4, 5],
                                                       "tibia": 85
                                                   }
                                           },
                                           "inverted": [2, 5, 8, 11]
                               },
                               debug = True, debug_wamp = True)
    runner.run(PhysicalModel)