
import GeneralMove

class Test(GeneralMove.Move):
    def __init__(self, *args, **kwds):
        GeneralMove.Move.__init__(self, *args, **kwds)
        self.caption = "Test"

    def tasks(self):
        return (("sleep", 0.1),
                ("rotate_body",),
                ("sleep", 0.1),
                ("shift_body_angle", 0),
                ("sleep", 0.1),
                ("shift_body_angle", 90),
                ("sleep", 0.1),
                ("shift_body_angle", 180),
                ("sleep", 0.1),
                ("shift_body_angle", 270),
                ("sleep", 0.1),
                ("shift_body_offset", 10, 10),
                ("sleep", 0.1),
                ("shift_body_offset", 0, -20),
                ("sleep", 0.1),
                ("shift_body_offset", -20, 0),
                ("sleep", 0.1),
                ("shift_body_offset", 0, 20),
                ("sleep", 0.1),
                ("shift_body_offset", 20, 0),
                ("sleep", 0.1),
                ("make_step", 0),
                ("sleep", 0.1),
                ("make_step", 90),
                ("sleep", 0.1),
                ("make_step", 180),
                ("sleep", 0.1),
                ("make_step", 270),
                ("sleep", 0.1))
