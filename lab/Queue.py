#!/usr/bin/env python3

from threading import Lock, Semaphore, Condition


class SynchronizedQueueSemaphore:
    def __init__(self):
        # Queue Initialization
        self.queue = []
        # Locks
        self.emptySemaphore = Semaphore()
        self.fullSemaphore = Semaphore()

    def size(self):
        return len(self.queue)

    def empty(self):
        return not self.size()

    def put(self, item):
        self.queue.append(item)
        self.emptySemaphore.release()

    def get(self):
        while not self.size():
            self.emptySemaphore.acquire()
        item = self.queue.pop(0)
        self.fullSemaphore.release()
        return item


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


class Queue:
    def __init__(self):
        # Queue Initialization
        self.queue = []


    def size(self):
        return len(self.queue)


    def empty(self):
        return not self.size()

    def put(self, item):
        self.queue.append(item)

    def get(self):
            item = self.queue.pop(0)
            return item
