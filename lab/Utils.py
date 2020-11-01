#!/usr/bin/env python3

import cv2
import os


class Utils(object):

  @staticmethod
  def getFrameSize(clipFileName):
    size = cv2.VideoCapture(clipFileName).get(cv2.CAP_PROP_FRAME_COUNT)
    return int(size)

  @staticmethod
  def debugger(count, debuggerLineCount=25):
    return count % debuggerLineCount == 0
