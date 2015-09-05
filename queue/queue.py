__author__ = 'romick'

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.python.failure import Failure
from autobahn.wamp import register
from autobahn.twisted.wamp import ApplicationSession
import Queue

# DEBUG = True


class CommandQueue(ApplicationSession):
    """
    A worker to hold queue
    """
    @inlineCallbacks
    def onJoin(self, details):
        print("queue session attached")
        self.q = Queue.Queue()
        results = yield self.register(self)
        for res in results:
            if isinstance(res, Failure):
                print("Failed to register procedure: {}".format(res.value))
            else:
                print("registration ID {}: {}".format(res.id, res.procedure))

    @register(u'com.tetry.queue.get_next')
    def queue_get_next(self):
        self.printer(u'wamp.metaevent.session.on_join')
        return self.q.get()

    @register(u'com.tetry.queue.append')
    def queue_append(self, command):
        # TODO: code to translate message to list of positions
        # self.printer(u'com.tetry.run_command', msg)
        return self.q.put(command)

    def printer(self, event, msg):
        print("Queue: {}: {}".format(event, msg))

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(CommandQueue)