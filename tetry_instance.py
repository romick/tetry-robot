import sys
import inspect
import datetime
import time

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession

import Crawler

DEBUG = True


class TetryInstance(ApplicationSession):
    """
    An application component that subscribes and receives events,
    and stop after having received 5 events.
    """

    # def __init__(self, *args):
    #     # self.bot = None
    #     ApplicationSession.__init__(self, args)

    @inlineCallbacks
    def sender(self, **kwds):
        if 'bot_command' in kwds:
            yield self.publish('com.tetry.servo_targets', kwds['bot_command'])
            yield self.logger(2, kwds['bot_command'])
        if 'message' in kwds:
            res = yield self.call('com.tetry.send2com', kwds['message'])
            yield self.publish('com.tetry.sent2com', kwds['message'])
            yield self.logger(2, kwds['message'])

    def logger(self, level, *args, **kwds):
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        calling_frame = inspect.getouterframes(inspect.currentframe(), 2)
        record = st, calling_frame[1][1], calling_frame[1][2], calling_frame[1][3], args, kwds
        if DEBUG:
            if level < 0:
                print >> sys.stderr, record
            else:
                print(record)
        self.publish("com.tetry.log", record)

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        # subscribe all methods on this object decorated with "@wamp.subscribe"
        # as PubSub event handlers
        #
        results = yield self.subscribe(self)
        for success, res in results:
            if success:
                # res is an Subscription instance
                print("Ok, subscribed handler with subscription ID {}".format(res.id))
            else:
                # res is an Failure instance
                print("Failed to subscribe handler: {}".format(res.value))

        self.bot = Crawler.Controller(sender=self.sender, logger=self.logger)
        self.bot.load_settings("../Robots/tetry.json")

    @inlineCallbacks
    @wamp.subscribe(u'com.tetry.run_command')
    def on_command(self, i):
        # try:
            print("Got event on run_command: {}".format(i))
            # self.received += 1
            # if self.received > 5:
            #     self.leave()
            # print(self.received)

            # print(i)
            print(i[u'command'])
            if hasattr(self.bot, i[u'command']):
                print("Got connected command: {}".format([u'command']))
                func = getattr(self.bot, i[u'command'])
                result = yield func(int(i[u'data']))
            else:
                print("function not found")
        # except Exception, e:
        #     print e

    @wamp.subscribe(u'com.tetry.log')
    def on_log(self, msg):
        print("Got event on log: {}".format(msg))

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(TetryInstance)