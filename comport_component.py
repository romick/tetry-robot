__author__ = 'romick'

import sys
if sys.platform == 'win32':
    ## on windows, we need to use the following reactor for serial support
    ## http://twistedmatrix.com/trac/ticket/3802
    ##
    from twisted.internet import win32eventreactor

    win32eventreactor.install()

from twisted.internet import reactor

from twisted.internet.defer import inlineCallbacks
from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import LineReceiver

from autobahn.twisted.wamp import ApplicationSession


class McuProtocol(LineReceiver):
    """
    MCU serial communication protocol.
    """

    ## need a reference to our WS-MCU gateway factory to dispatch PubSub events
    ##
    def __init__(self, session, debug=False):
        self.debug = debug
        self.session = session


    def connectionMade(self):
        print('Serial port connected.')


    def lineReceived(self, line):
        if self.debug:
            print("Serial RX: {0}".format(line))
        self.session.publish(u"com.tetry.got_from_com", line)


    def send_command(self, command):
        """
        This method is exported as RPC and can be called by connected clients
        """
        command = command.encode('ascii')
        if self.debug:
            print("Serial TX: {0}".format(command))
        self.transport.write(command)


class McuComponent(ApplicationSession):
    """
    MCU WAMP application component.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("MyComponent ready! Configuration: {}".format(self.config.extra))

        port = self.config.extra['port']
        baudrate = self.config.extra['baudrate']
        debug = self.config.extra['debug']

        serialProtocol = McuProtocol(self, debug)


        print('About to open serial port {0} [{1} baud] ..'.format(port, baudrate))
        try:
            serialPort = SerialPort(serialProtocol, port, reactor, baudrate=baudrate)
        except Exception as e:
            print('Could not open serial port: {0}'.format(e))
            self.leave()
        else:
            yield self.register(serialProtocol.send_command, u"com.tetry.send2com")

if __name__ == '__main__':
    #

    print("Using Twisted reactor {0}".format(reactor.__class__))
    from autobahn.twisted.wamp import ApplicationRunner
    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", u"realm1",
                               extra = {'port': "/dev/pts/2", 'baudrate': 115200, 'debug': True},
                               debug = True, debug_wamp = True)
    runner.run(McuComponent)