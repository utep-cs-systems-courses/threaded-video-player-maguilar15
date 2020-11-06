#!/usr/bin/env python3

from threading import Semaphore, Lock

class QueueSemaphore:
    def __init__(self, value=10):
        # Queue Initialization
        self.queue = []
        # Locks
        self.lock = Lock()
        self.fullSemaphore = Semaphore(value=value)
        self.emptySemaphore = Semaphore(value=0)

    def size(self):
        return len(self.queue)

    def empty(self):
        return not self.size()

    def put(self, item):
        self.fullSemaphore.acquire()
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.emptySemaphore.release()

    def get(self):
        while not self.size():
            self.emptySemaphore.acquire()
        self.lock.acquire()
        item = self.queue.pop(0)
        self.lock.release()
        self.fullSemaphore.release()
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
