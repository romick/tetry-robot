__author__ = 'romick'

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.python.failure import Failure
from autobahn.wamp import register
from autobahn.twisted.wamp import ApplicationSession
from TetryTools import MathTools

# DEBUG = True
MY_DRIVE_SPEED_MIN = 500
MY_DRIVE_SPEED_MAX = 2500


class CommandConverter(ApplicationSession):
    """
    A worker to convert angles to servo commands
    """
    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        print("component created")
        self.model = None
        self.protocol = None

    @inlineCallbacks
    def onJoin(self, details):
        print("command_converter session attached")
        results = yield self.register(self)
        for res in results:
            if isinstance(res, Failure):
                print("Failed to register procedure: {}".format(res.value))
            else:
                print("registration ID {}: {}".format(res.id, res.procedure))
        self.model = yield self.call(u'com.tetry.get_model')
        self.protocol = self.model["protocol"]
        # protocols = ['Custom tetry', 'Compact', 'Pololu', 'MiniSSC']
        # if not self.protocol:
        #     self.current_protocol = self.protocols[0]
        self.printer(1, "Protocol is %s" % self.protocol)

    @register(u'com.tetry.convert_command')
    def convert_command(self, bot_command):
        message = ''

        bot_command = self._angles2positions(bot_command)
        if self.protocol == 'Custom tetry':
            for x in bot_command:
                message += '#%iP%i' % (x['servo'], x['position'])
                # self.sliders[x['servo']].SetValue(x['position'])
            # message = message[::-1]
            message += '\n'

        elif self.protocol == 'Compact':
            if len(bot_command) > 1:
                # Set Multiple Targets
                # Compact current_protocol:
                # 0x9F,
                # number of targets,
                # first channel number,
                # first target low bits,
                # first target high bits,
                # second target low bits,
                # second target high bits,
                # ...
                message = chr(0x9F) + chr(len(bot_command))
                for x in bot_command:
                    posi = x['position'] * 4
                    message = message + \
                              chr(x['servo']) + \
                              chr(posi & 0x7F) + \
                              chr((posi >> 7) & 0x7F)
            else:
                posi = bot_command[0]['position'] * 4
                message = chr(84) + \
                          chr(bot_command[0]['servo']) + \
                          chr(posi & 0x7F) + \
                          chr((posi >> 7) & 0x7F)

        elif self.protocol == 'Pololu':
            pololu_device_number = 12
            if len(bot_command) > 1:
                # Set Multiple Targets
                # Pololu current_protocol:
                # 0xAA,
                # device number,
                # 0x1F,
                # number of targets,
                # first channel number,
                # first target low bits,
                # first target high bits,
                # second target low bits,
                # second target high bits,
                # ...
                message = chr(0xAA) + chr(pololu_device_number) + chr(0x1F) + chr(len(bot_command))
                for x in bot_command:
                    posi = x['position'] * 4
                    message = message + \
                              chr(x['servo']) + \
                              chr(posi & 0x7F) + \
                              chr((posi >> 7) & 0x7F)
            else:
                posi = bot_command[0]['position'] * 4
                message = chr(0xAA) + \
                          chr(pololu_device_number) + \
                          chr(4) + \
                          chr(bot_command[0]['servo']) + \
                          chr(posi & 0x7F) + \
                          chr((posi >> 7) & 0x7F)

        elif self.protocol == 'MiniSSC':
            self.logger(1, "MiniSSC current_protocol has not been implemented yet!")

        else:
            self.logger(1, "No current_protocol defined!")
        return message

    def _angles2positions(self, alist):
        plist = []
        for a in alist:
            if 'position' not in a.keys():
                if a['servo'] in self.model["inverted"]:
                    a['position'] = int(round(
                        MathTools.interpolate(a['angle'], 180, -180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX)
                    ))
                else:
                    a['position'] = int(round(
                        MathTools.interpolate(a['angle'], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX)
                    ))
            plist.append(a)
        return plist

    def printer(self, event, msg):
        print("CommandConverter: {}: {}".format(event, msg))

    def logger(self, *wds):
        print wds

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", "realm1")
    print "started"
    runner.run(CommandConverter)