
import math

class MathTools():

    @staticmethod
    def coordinates2angle(*args):
        print args
        angle = math.degrees(math.atan2(args[0], args[1]))
        if angle < 0:
            angle += 360
        return angle

    #TODO: make angle2coordinates method
    @staticmethod
    def angle2coordinates(*args):
        """Not implemented yet."""
        pass
