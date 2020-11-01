#!/usr/bin/env python3

from threading import Thread, Semaphore
from Utils import Utils
import cv2,os

frameQueue = []
greyQueue = []
clipFileName = "clip.mp4"
stdout = False
debuggerLineCount = 25
outputDir = "./frameData"

framesToLoad = Utils().getFrameSize(clipFileName)


def extractFrame(semaphore):
        global frameQueue
        count = 0

        # open the video clip
        vidcap = cv2.VideoCapture(clipFileName)

        # read one frame
        success, image = vidcap.read()

        # Critical Section
        while success and framesToLoad:
            # Frames to Queue1
            frameQueue.append(image)


            success, image = vidcap.read()

            # Debugger
            if Utils().debugger(count):
                print(f"[Thread 1] Reading Frame Count: {count} of {framesToLoad}, Status: {success}")

            # Create Frames
            if True:
                if not os.path.exists("./frameData"):
                    os.makedirs("frameData")
                try:
                    # write the current frame out as a jpeg image
                    cv2.imwrite(f"frameData/frame_{count:04d}.bmp", image)
                except Exception as e:
                    print(f"Exception={e}")
            count += 1


def convertToGrayScale(semaphore):
        global frameQueue, greyQueue
        count = 0

        # Critical Section
        while count < framesToLoad:
            semaphore.acquire()
            # Debugger
            if Utils().debugger(count):
                print(f"[Thread 2] Converting frame {count} of {framesToLoad}")

            pop = greyQueue.pop()
            # convert the image to grayscale
            grayscaleFrame = cv2.cvtColor(pop, cv2.COLOR_BGR2GRAY)
            count += 1

            # Add Frame to Queue 2
            greyQueue.append(grayscaleFrame)
        semaphore.release()

def display(semaphore):
        global greyQueue
        count = 0
        frameDelay = 42

        # Critical Section
        while greyQueue:
            frame = greyQueue.pop()

            # Debugger
            if Utils().debugger(count):
                print(f"[Thread 3] Displaying Frame {count} of {framesToLoad}")

            # Wait for 42 ms and check if the user wants to quit
            cv2.imshow("video", frame)
            if (cv2.waitKey(frameDelay) and 0xFF == ord("q") or count == framesToLoad):
                break
            count += 1

        cv2.destroyAllWindows()

def main():
    semaphore = Semaphore(3)
    Thread(target=extractFrame,args=(semaphore,)).start()
    Thread(target=convertToGrayScale,args=(semaphore,)).start()
    Thread(target=display,args=(semaphore,)).start()

if __name__ == '__main__':
    main()