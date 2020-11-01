from threading import Lock,Condition

class Queue:

    def __init__(self):
        self.queue = []
        self.lock = Lock()
        self.not_full = Condition(self.lock)

    def empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def put(self, x):
        with self.not_full:
            self._put(x)

    def get(self):
        return self._get()

    def _put(self, x):
        self.queue.append(x)


    def _get(self):
        with self.not_full:
            pop = self.queue.pop()
            return pop