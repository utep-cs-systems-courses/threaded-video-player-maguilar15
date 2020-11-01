#!/usr/bin/env python3

import cv2
import os


class Utils(object):
  def __init__(self):
    pass

  def getFrameSize(self, clipFileName):
    size = cv2.VideoCapture(clipFileName).get(cv2.CAP_PROP_FRAME_COUNT)
    return int(size)

  def debugger(self, count, debuggerLineCount=25):
    return count % debuggerLineCount == 0
