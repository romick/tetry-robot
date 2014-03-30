
import GeneralMove

class Reset(GeneralMove.Move):
    def __init__(self, *args, **kwds):
        GeneralMove.Move.__init__(self, *args, **kwds)
        self.caption = "Reset"

    def tasks(self):
        return (("init_bot", ), )
