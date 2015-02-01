import sys
import inspect
import datetime
import time

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession

import Crawler


class Component(ApplicationSession):
    """
    An application component that subscribes and receives events,
    and stop after having received 5 events.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        ## subscribe all methods on this object decorated with "@wamp.subscribe"
        ## as PubSub event handlers
        ##
        results = yield self.subscribe(self)
        for success, res in results:
            if success:
                ## res is an Subscription instance
                print("Ok, subscribed handler with subscription ID {}".format(res.id))
            else:
                ## res is an Failure instance
                print("Failed to subscribe handler: {}".format(res.value))


    @wamp.subscribe(u'com.tetry.run_command')
    def onCommand(self, i):
        # try:
            print("Got event on run_command: {}".format(i))
            # self.received += 1
            # if self.received > 5:
            #     self.leave()
            # print(self.received)

            # print(i)
            print(i[u'command'])
            if hasattr(bot, i[u'command']):
                print("Got connected command: {}".format([u'command']))
                func = getattr(bot, i[u'command'])
                result = func(int(i[u'data']))
            else:
                print("function not found")
        # except Exception, e:
        #     print e


    @wamp.subscribe(u'com.myapp.topic2')
    def onEvent2(self, msg):
        print("Got event on topic2: {}".format(msg))


    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    def dummysender(**kwds):
        print(kwds)

    def dummylogger(level, *args, **kwds):
        """
        Placeholder for logger

        """
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        calling_frame = inspect.getouterframes(inspect.currentframe(), 2)
        record = (st, calling_frame[1][1:4], args, kwds)
        # log_q.put(record)
        if level < 0:
            print >> sys.stderr, record
        else:
            print(record)

    from autobahn.twisted.wamp import ApplicationRunner

    bot = Crawler.Controller(sender=dummysender, logger=dummylogger)
    bot.load_settings("./Robots/tetry.json")

    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(Component)