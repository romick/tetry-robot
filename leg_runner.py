__author__ = 'romick'
__author__ = 'romick'

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession

class LegRunner(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        ## session metaevents: these are fired by Crossbar.io
        ## upon _other_ WAMP sessions joining/leaving the router
        ##
        results = yield self.subscribe(self)
        for success, res in results:
            if success:
                # res is an Subscription instance
                print("Ok, subscribed handler with subscription ID {}".format(res.id))
            else:
                # res is an Failure instance
                print("Failed to subscribe handler: {}".format(res.value))
        print "Leg_runner started"
        # self.call()

if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(LegRunner)