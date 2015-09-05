__author__ = 'romick'
import traceback
import sys

# if sys.platform == 'win32':
#     # on windows, we need to use the following reactor for serial support
#     # http://twistedmatrix.com/trac/ticket/3802
#     #
#     from twisted.internet import win32eventreactor
#
#     win32eventreactor.install()
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from leg_IK import legIK


class LegRunner(ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        self.name = self.config.extra['name']
        # print(details)

        print("Leg_runner with name {} started".format(self.name))
        try:
            yield self.register(self.init, 'com.tetry.{}.init'.format(self.name))
            yield self.register(self.get_starting_point, 'com.tetry.{}.get_starting_point'.format(self.name))
            yield self.register(self.get_to_offset, 'com.tetry.{}.get_to_offset'.format(self.name))
            yield self.register(self.get_to_offset_from_initial, 'com.tetry.{}.get_to_offset_from_initial'.format(self.name))
            yield self.register(self.get_rotate, 'com.tetry.{}.get_rotate'.format(self.name))
        except Exception as e:
            traceback.print_exc()
            # pass

    def init(self, model):
        # print "Leg's model is: ", model
        self.leg = legIK.Leg(logger=self.logger,
                             offset=model['offset'],
                             coxa=model['coxa'],
                             temur=model['temur'],
                             tibia=model['tibia'],
                             servos=model['servos'],
                             initial_state=model['initial_state'],
                             name=model['name'],
                             id=model['id'],
                             debug=model['debug'])
        # print("Leg created!")
        return 1

    def get_starting_point(self):
        return self.leg.set_initial_state()
        # return 1

    def get_rotate(self, matrix):
        return self.leg.rotate(matrix)
        # return 1

    def get_to_offset_from_initial(self, x, y, z):
        return self.leg.go_offset(x, y, z)
        # return 1

    def get_to_offset(self, x, y, z):
        return self.leg.go_offset_from_initial(x, y, z)
        # return 1

    def logger(self, *args):
        print (args)


if __name__ == '__main__':
    from autobahn.twisted.wamp import ApplicationRunner

    runner = ApplicationRunner("ws://127.0.0.1:8080/ws", u"realm1", extra={"name": "dummy"})
    print "started"
    runner.run(LegRunner)