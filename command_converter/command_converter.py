__author__ = 'romick'

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.python.failure import Failure
from autobahn.wamp import register
from autobahn.twisted.wamp import ApplicationSession


# DEBUG = True


class CommandConverter(ApplicationSession):
    """
    A worker to hold queue
    """
    @inlineCallbacks
    def onJoin(self, details):
        print("command_converter session attached")
        results = yield self.register(self)
        for res in results:
            if isinstance(res, Failure):
                print("Failed to register procedure: {}".format(res.value))
            else:
                print("registration ID {}: {}".format(res.id, res.procedure))
        model = yield self.call(u'com.tetry.get_model')
        protocol = model["protocol"]
        self.protocols = ['Custom tetry', 'Compact', 'Pololu', 'MiniSSC']
        if not protocol:
            self.current_protocol = self.protocols[0]
        self.printer(1, "Protocol is %s" % self.current_protocol)

    @register(u'com.tetry.convert_command')
    def convert_command(self):
        # self.printer(u'wamp.metaevent.session.on_join')
        return self.q.get()

    def printer(self, event, msg):
        print("Queue: {}: {}".format(event, msg))

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(CommandConverter)