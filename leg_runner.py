__author__ = 'romick'
import sys
if sys.platform == 'win32':
    # on windows, we need to use the following reactor for serial support
    # http://twistedmatrix.com/trac/ticket/3802
    #
    from twisted.internet import win32eventreactor
    win32eventreactor.install()
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession


class LegRunner(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        ## session metaevents: these are fired by Crossbar.io
        ## upon _other_ WAMP sessions joining/leaving the router
        ##
        self.name = self.config.extra['name']
        print(details)

        results = yield self.subscribe(self)
        for success, res in results:
            if success:
                # res is an Subscription instance
                print("Ok, subscribed handler with subscription ID {}".format(res.id))
            else:
                # res is an Failure instance
                print("Failed to subscribe handler: {}".format(res.value))
        print("Leg_runner with name {} started".format(self.name))
        # self.call()
        try:
            yield self.register(self.init, 'com.tetry.{}.init'.format(self.name))
        except Exception as e:
            pass
        # else:
        #     print("fail :^(")

    def init(self, model):
        pass

if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", u"realm1", extra={"name":"dummy"})
    print "started"
    runner.run(LegRunner)