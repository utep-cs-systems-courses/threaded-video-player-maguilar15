#!/usr/bin/env python3

from lab.VideoPlayer import VideoPlayer

# Constants
fileName = "clip.mp4"
frameCountLineDebugger = 20
saveFrames = False
outputDir = "./frameData"
color = False


if __name__ == "__main__":

    videoPlayer = VideoPlayer(clipFileName=fileName,
                              frameCountLineDebugger=frameCountLineDebugger,
                              stdout=saveFrames,
                              colorFrames=color
                              )

    videoPlayer.start()
