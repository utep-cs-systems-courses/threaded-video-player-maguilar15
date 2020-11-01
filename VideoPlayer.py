#!/usr/bin/env python3

from threading import Thread, Semaphore
from Utils import Utils
from Queue import Queue
import cv2, os
from queue import Queue as SynchronizedQueue


class VideoPlayer(object):

    def __init__(self, clipFileName, frameCountLineDebugger=25, semaphoreValue=24,stdout=False,outputDir=None):
        self.semaphore = Semaphore(semaphoreValue)
        self.clipFileName = clipFileName
        self.framesToLoad = Utils().getFrameSize(clipFileName)
        self.frameCountLineDebugger = frameCountLineDebugger
        self.frameQueue = SynchronizedQueue()
        self.grayQueue = SynchronizedQueue()
        self.stdout = stdout
        self.outputDir = outputDir


    def start(self):
        Thread(target=self.extractFrame, name="Extract Frames").start()
        Thread(target=self.convertToGrayScale, name="Convert to Grayscale").start()
        Thread(target=self.display(), name="Display Video").start()


    def extractFrame(self):
        count = 0

        # open the video clip
        vidcap = cv2.VideoCapture(self.clipFileName)

        # read one frame
        success, image = vidcap.read()

        # Critical Section
        while success and count < self.framesToLoad:
            self.semaphore.acquire()

            # Frames to Queue1
            self.frameQueue.put(image)

            success, image = vidcap.read()

            # Debugger
            if Utils().debugger(count=count,debuggerLineCount=self.frameCountLineDebugger):
                print(f"[Thread 1] Reading Frame Count: {count} of {self.framesToLoad}, Status: {success}")

            # Create Frames
            if self.stdout:
                if not os.path.exists(self.outputDir):
                    os.makedirs(self.outputDir)
                # write the current frame out as a jpeg image
                cv2.imwrite(f"{self.outputDir}/frame_{count:04d}.bmp", image)

            count += 1
            self.semaphore.release()

    def convertToGrayScale(self):
        count = 0

        # Critical Section
        while count < self.framesToLoad:
            self.semaphore.acquire()

            # Debugger
            if Utils().debugger(count,self.frameCountLineDebugger):
                print(f"[Thread 2] Converting frame {count} of {self.framesToLoad}")

            # convert the image to grayscale
            grayscaleFrame = cv2.cvtColor(self.frameQueue.get(), cv2.COLOR_BGR2GRAY)
            count += 1

            # Add Frame to Queue 2
            self.grayQueue.put(grayscaleFrame)
            self.semaphore.release()

    def display(self):
        count = 0
        frameDelay = 42

        # Critical Section
        while self.grayQueue:
            self.semaphore.acquire()

            frame = self.grayQueue.get()

            # Debugger
            if Utils().debugger(count=count,debuggerLineCount=self.frameCountLineDebugger):
                print(f"[Thread 3] Displaying Frame {count} of {self.framesToLoad}")

            # Wait for 42 ms and check if the user wants to quit
            cv2.imshow("video", frame)
            if (cv2.waitKey(frameDelay) and 0xFF == ord("q") or self.grayQueue.empty()):
                break
            count += 1
            self.semaphore.release()

        cv2.destroyAllWindows()

