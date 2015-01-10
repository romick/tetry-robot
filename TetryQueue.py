import Queue

__author__ = 'romick'


class TetryQueue(Queue.Queue):
    def __getitem__(self, index):
        with self.mutex:
            return self.queue[index]