#!/usr/bin/env python3

from threading import Semaphore

class SemaphoreQueue:
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
