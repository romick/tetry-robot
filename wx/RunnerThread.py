import threading
import time

__author__ = 'romick'


class RunnerThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            if not self.queue.empty():
                task = self.queue.get()
                print task
                task[0](*task[1:])
            else:
                time.sleep(0.1)