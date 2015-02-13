__author__ = 'romick'

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession

DEBUG = True


class EventCatcher(ApplicationSession):
    """
    An application component that subscribes and receives events
    """
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

    @wamp.subscribe(u'wamp.metaevent.session.on_join')
    def on_command(self, msg):
        self.printer(u'wamp.metaevent.session.on_join', msg)

    @wamp.subscribe(u'com.tetry.run_command')
    def on_command(self, msg):
        self.printer(u'com.tetry.run_command', msg)

    @wamp.subscribe(u'com.tetry.log')
    def on_log(self, msg):
        self.printer(u'com.tetry.log', msg)

    @wamp.subscribe(u'com.tetry.got_from_com')
    def on_com_line(self, msg):
        self.printer(u'com.tetry.got_from_com', msg)

    @wamp.subscribe(u'com.tetry.servo_targets')
    def on_com_line(self, msg):
        self.printer(u'com.tetry.servo_targets', msg)

    @wamp.subscribe(u'com.tetry.sent2com')
    def on_com_line(self, msg):
        self.printer(u'com.tetry.sent2com', msg)

    # @wamp.subscribe()
    # def on_com_line(self, msg):
    #     self.printer(, msg)

    def printer(self, event, msg):
        print("Event catcher: {}: {}".format(event, msg))

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(EventCatcher)