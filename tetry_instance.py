import sys
import traceback
import inspect
import datetime
import time

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.python.failure import Failure
from autobahn.wamp import subscribe
from autobahn.twisted.wamp import ApplicationSession

import Crawler

DEBUG = False


class TetryInstance(ApplicationSession):
    """
    An application component that subscribes and receives events,
    and stop after having received 5 events.
    """

    # @inlineCallbacks
    def __init__(self, config = None):
        ApplicationSession.__init__(self, config)
        print("component created")

    # @inlineCallbacks
    def sender(self, **kwds):
        print kwds
        if 'bot_command' in kwds:
            self.publish('com.tetry.servo_targets', kwds['bot_command'])
            self.logger(2, kwds['bot_command'])
        if 'message' in kwds:
            res = self.call('com.tetry.send2com', kwds['message'])
            self.publish('com.tetry.sent2com', kwds['message'])
            # self.logger(2, kwds['message'])

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
        print("tetry instance session attached")

        # subscribe all methods on this object decorated with "@wamp.subscribe"
        # as PubSub event handlers
        #
        results = yield self.subscribe(self)
       # check we didn't have any errors
        for sub in results:
            if isinstance(sub, Failure):
                print("subscribe failed:", sub.getErrorMessage())

        self.bot = Crawler.Controller(sender=self.sender, logger=self.logger, app=self)
        try:
            self.model = yield self.call('com.tetry.get_model')
            yield self.bot.load_settings(self.model)
            print("Loading model...")
        except Exception as e:
            # print(e.message)
            traceback.print_exc()
        # print(self.model)


    @inlineCallbacks
    @subscribe(u'com.tetry.run_command')
    def on_command(self, i):
        # try:
            print("Got event on run_command: {}".format(i))
            # print(i)
            # print(i[u'command'])
            if hasattr(self.bot, i[u'command']):
                print("Found connected command: {}".format(i[u'command']))
                func = getattr(self.bot, i[u'command'])
                result = yield func(int(i[u'data']))
            else:
                print("function not found")
        # except Exception, e:
        #     print e

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(TetryInstance)