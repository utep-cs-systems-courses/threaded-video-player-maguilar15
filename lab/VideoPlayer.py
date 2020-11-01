#!/usr/bin/env python3

from threading import Thread, Semaphore
from lab.Utils import Utils
from lab.Queue import Queue, SynchronizedQueue, SynchronizedQueueSemaphore
import cv2, os


class VideoPlayer(object):

    def __init__(self, clipFileName, frameCountLineDebugger=25, semaphoreValue=24, stdout=False, outputDir="frameData", colorFrames=False):
        # Lock
        #self.semaphore = Semaphore(semaphoreValue)
        # Data Fields
        self.clipFileName = clipFileName
        self.framesToLoad = Utils.getFrameSize(clipFileName)
        self.frameCountLineDebugger = frameCountLineDebugger
        # Queues
        self.frameQueue = SynchronizedQueueSemaphore()
        self.grayQueue = SynchronizedQueueSemaphore()
        # Options
        self.stdout = stdout
        self.outputDir = outputDir
        self.colorFrames = colorFrames


    def start(self):
        Thread(target=self.extractFrame, name="Extract Frames",daemon=True).start()
        Thread(target=self.convertToGrayScale, name="Convert to Grayscale",daemon=True).start()
        Thread(target=self.display(), name="Display Video",daemon=True).start()


    def extractFrame(self):
        count = 0

        # open the video clip
        vidcap = cv2.VideoCapture(self.clipFileName)

        # read one frame
        success, image = vidcap.read()

        # Critical Section
        while success:
            #self.semaphore.acquire()

            # Frames to Queue1
            self.frameQueue.put(image)

            success, image = vidcap.read()

            # Debugger
            if Utils.debugger(count=count,debuggerLineCount=self.frameCountLineDebugger):
                print(f"[Thread 1] Reading Frame Count: {count} of {self.framesToLoad}, Status: {success}")

            # Create Frames
            if self.stdout:
                if not os.path.exists(self.outputDir):
                    os.makedirs(self.outputDir)
                # write the current frame out as a jpeg image
                cv2.imwrite(f"{self.outputDir}/frame_{count:04d}.bmp", image)

            count += 1
            #self.semaphore.release()


    def convertToGrayScale(self):
        count = 0

        # Critical Section
        while count < self.framesToLoad:
            #self.semaphore.acquire()

            # Debugger
            if Utils.debugger(count,self.frameCountLineDebugger):
                print(f"[Thread 2] Converting frame {count} of {self.framesToLoad}")

            if self.colorFrames:
                grayscaleFrame = cv2.cvtColor(self.frameQueue.get(), cv2.COLOR_BGR2RGB)
            else:
                grayscaleFrame = cv2.cvtColor(self.frameQueue.get(), cv2.COLOR_BGR2GRAY)

            count += 1

            # Add Frame to Queue 2
            self.grayQueue.put(grayscaleFrame)
            #self.semaphore.release()


    def display(self):
        count = 0
        frameDelay = 42

        # Critical Section
        while self.grayQueue:
            #self.semaphore.acquire()

            frame = self.grayQueue.get()

            # Debugger
            if Utils.debugger(count=count,debuggerLineCount=self.frameCountLineDebugger):
                print(f"[Thread 3] Displaying Frame {count} of {self.framesToLoad}")

            # Wait for 42 ms and check if the user wants to quit
            cv2.imshow("Video", frame)
            if (cv2.waitKey(frameDelay) and 0xFF == ord("q") or self.grayQueue.empty()):
                break
            count += 1
            #self.semaphore.release()

        cv2.destroyAllWindows()

