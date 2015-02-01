
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession



class Component(ApplicationSession):
   """
   An application component that publishes an event every second.
   """

   @inlineCallbacks
   def onJoin(self, details):
      print("session attached")
      counter = 0
      while True:
         print(".")
         self.publish('com.tetry.run_command', counter)
         counter += 1
         yield sleep(1)



if __name__ == '__main__':
   from autobahn.twisted.wamp import ApplicationRunner
   runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
   runner.run(Component)