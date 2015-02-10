__author__ = 'romick'

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession

class TetrySuperviser(ApplicationSession):

   @inlineCallbacks
   def onJoin(self, details):

      ## session metaevents: these are fired by Crossbar.io
      ## upon _other_ WAMP sessions joining/leaving the router
      ##

      @inlineCallbacks
      def on_session_join(details):
         print("on_session_join: {}".format(details))

      yield self.subscribe(on_session_join, 'wamp.metaevent.session.on_join')


      @inlineCallbacks
      def on_session_leave(details):
         print("on_session_leave: {}".format(details))

      yield self.subscribe(on_session_leave, 'wamp.metaevent.session.on_leave')

      # res = yield self.call('crossbar.node.9774.get_info')
      # print res


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(TetrySuperviser)