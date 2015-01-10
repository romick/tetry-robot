import math
import numpy
# import sys


class Leg:
    """ new legIK(offset=[-65.8, 76.3], angle=-2.2829, coxa=29.0, temur=49, tibia=52)  docstring for legIK"""

    #TODO: rewrite- each part of the leg should be a Vector
    def __init__(self, **kwds):
        self.logger = kwds['logger']
        self.leg_offset = kwds['offset']
        self.coxa_length = kwds['coxa']
        self.temur_length = kwds['temur']
        self.tibia_length = kwds['tibia']
        self.servos = kwds['servos']
        self.initial_state = kwds['initial_state']
        self.name = kwds['name']
        self.id = kwds['id']
        self.state_x = 0
        self.state_y = 0
        self.state_z = 0
        if 'debug' in kwds.keys():
            self.debug = kwds['debug']
        else:
            self.debug = False
        self.leg_offset_angle = math.atan2(self.leg_offset[0], self.leg_offset[1])
        if self.leg_offset_angle < 0:
            self.leg_offset_angle += 2 * math.pi
        if self.debug:
            self.logger(1, self.name, ": leg_offset_angle(radians)=", self.leg_offset_angle)
            self.logger(1, self.name, ": leg_offset_angle(degrees)=", math.degrees(self.leg_offset_angle))

    def _ik_lower_leg(self, x, y):
        #self.logger(1, "IK function called. x=", x, "y=", y)
        if self.debug:
            self.logger(1, "Lower leg targets are:", x, y)
        try:
            d = math.sqrt(x ** 2 + y ** 2)
            k = (d ** 2 - self.tibia_length ** 2 + self.temur_length ** 2) / (2 * d)
            m = math.sqrt(self.temur_length ** 2 - k * k)
        except ZeroDivisionError:
            if self.debug:
                self.logger(1, "Divide by Zero error. No valid joint solution.")
            return
        except ValueError:
            if self.debug:
                self.logger(1, "Math function error. Probably square root of negative number. No valid joint solution.")
            return
        theta = math.degrees(math.atan2(float(y), float(x)) - math.atan2(m, k))
        phi = math.degrees(math.atan2(m, k) + math.atan2(m, (d - k)))
        return_angles = [theta, phi]
        #self.logger(1, "theta=", theta, "phi=", phi)
        return return_angles

    def _ik_full_leg(self, x, y, z):
        alpha = math.degrees(math.atan2(x, y))
        # if alpha < 0:
        # alpha = 360 + alpha
        lower_leg_angles = self._ik_lower_leg(math.sqrt(x ** 2 + y ** 2) - self.coxa_length, z)
        if lower_leg_angles is None:
            if self.debug:
                self.logger(1, "No ikFullLeg calculation available!")
            return
        else:
            if self.debug:
                self.logger(1, "ikFullLeg ", round(alpha), round(lower_leg_angles[0]), round(lower_leg_angles[1]))
            return_angles = [alpha, lower_leg_angles[0], lower_leg_angles[1]]
            return return_angles

    def _get_angles(self, x, y, z):
        if self.debug:
            self.logger(1, self.name, ": Global targets are:", x, y, z)
        #re-calculate position
        cos_angle = math.cos(self.leg_offset_angle)
        sin_angle = math.sin(self.leg_offset_angle)

        x = math.copysign((x - self.leg_offset[0]), sin_angle)
        y = math.copysign((y - self.leg_offset[1]), cos_angle)
        # rotate to leg zero position
        if self.debug:
            self.logger(1, "Cos_angle", cos_angle, "Sin_angle", sin_angle)
            self.logger(1, "Leg local targets in global coordinates are x=", x, " y=", y, "z=", z)
        leg_x = cos_angle * x - sin_angle * y
        leg_y = sin_angle * x + cos_angle * y
        # get IK solution and move leg
        if self.debug:
            self.logger(1, "Leg targets in local coordinates are legX=%.2f" % leg_x, " legY=%.2f" % leg_y, z)
        s = self._ik_full_leg(leg_x, leg_y, z)
        if s is None:
            if self.debug:
                self.logger(1, "No angles available!")
            return [0, 0, 0]
        else:
            #self.logger(1, "%.2f" % s[0], "%.2f" % s[1], "%.2f" % s[2])
            return s

    #def _getPositions (self, x, y, z):
    #    some = self._get_angles(x, y, z)
    #    some[0] = round(self._interpolate(some[0], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX))
    #    some[1] = round(self._interpolate(some[1], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX))
    #    some[2] = round(self._interpolate(some[2], -180, 180, MY_DRIVE_SPEED_MIN, MY_DRIVE_SPEED_MAX))
    #    if self.debug:
    #        self.logger(1, "Positions:", some)
    #    return some

    def go_exact_coordinates(self, x, y, z):

        #check if targets set
        if x is None:
            x = self.state_x
        if y is None:
            y = self.state_y
        if z is None:
            z = self.state_z

        #save current position
        self.state_x = int(x)
        self.state_y = int(y)
        self.state_z = int(z)
        #self.logger(-1, self.state_x, self.state_y, self.state_z)

        [xp, yp, zp] = self._get_angles(x, y, z)
        #self.logger(-1, xp,yp,zp)
        command_list = [dict(servo=self.servos[0], angle=int(xp)),
                        dict(servo=self.servos[1], angle=int(yp)),
                        dict(servo=self.servos[2], angle=int(zp))]
        return command_list

    def set_initial_state(self):
        return self.go_exact_coordinates(self.initial_state[0], self.initial_state[1], self.initial_state[2])

    def go_offset(self, x_offset, y_offset, z_offset):
        return self.go_exact_coordinates(self.state_x + x_offset, self.state_y + y_offset, self.state_z + z_offset)

    def go_offset_from_initial(self, x_offset, y_offset, z_offset):
        return self.go_exact_coordinates(self.initial_state[0] + x_offset,
                                         self.initial_state[1] + y_offset,
                                         self.initial_state[2] + z_offset)

    def rotate(self, rot_matrix):
        coordinates = numpy.array([self.state_x, self.state_y, self.state_z])
        coordinates = rot_matrix.dot(coordinates)
        return self.go_exact_coordinates(coordinates[0], coordinates[1],coordinates[2])  #TODO: Convert to correct way!