__author__ = 'romick'

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.python.failure import Failure
from autobahn.wamp import register
from autobahn.twisted.wamp import ApplicationSession
import time

# DEBUG = True


class Actor(ApplicationSession):
    """
    A worker to run command executor and balancer
    """
    @inlineCallbacks
    def onJoin(self, details):
        print("actor session attached")
        period = 100
        factor = 10000
        while 1:
            ts1 = int(time.time()*factor)
            q = yield self.call(u'com.tetry.queue.get_next')
            # TODO: add balancer code
            text_command = yield self.call(u'com.tetry.convert_command', q)
            res = yield self.call(u'com.tetry.send2ssc32', text_command)
            ts2 = int(time.time()*factor)
            td = ts2 - ts1
            if td < period:
                time.sleep((period-td)/factor)

    def printer(self, event, msg):
        print("Actor: {}: {}".format(event, msg))

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(Actor)