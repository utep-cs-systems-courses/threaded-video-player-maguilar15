from threading import Lock, Condition


class SynchronizedQueue:
    def __init__(self):
        # Queue Initialization
        self.queue = []
        # Locks
        self.lock = Lock()
        self.emptyCondition = Condition(self.lock)
        self.fullCondition = Condition(self.lock)


    def size(self):
        return len(self.queue)


    def empty(self):
        with self.lock:
            return not self.size()


    def put(self, item):
        with self.fullCondition:
            self.queue.append(item)
            self.emptyCondition.notify()


    def get(self):
        with self.emptyCondition:
            while not self.size():
                self.emptyCondition.wait()
            item = self.queue.pop(0)
            self.fullCondition.notify()
            return item

