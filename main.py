#!/usr/bin/env python3

from VideoPlayer import VideoPlayer

# Constants
fileName = "clip.mp4"
semaphoreCount = 3
frameCountLineDebugger = 20
saveFrames = False
outputDir = "./frameData"

if __name__ == "__main__":

    videoPlayer = VideoPlayer(clipFileName=fileName,
                              frameCountLineDebugger=frameCountLineDebugger,
                              semaphoreValue=semaphoreCount,
                              stdout=saveFrames,
                              outputDir=outputDir
                              )

    videoPlayer.start()
