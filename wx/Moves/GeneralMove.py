__author__ = 'Roman.Milovanov'


class Move():
    def __init__(self, *args, **kwds):
        self.bot = kwds['bot']
        self.runner = kwds['runner']
        self.caption = 'dummy'

    def run(self):
        for task in self.tasks():
            self.runner(*task)

    def tasks(self):
        return None