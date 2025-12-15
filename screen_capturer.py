import time

import cv2
import mss
import numpy as np


class Capture:
    def __init__(self, capture, timestamp=None):
        self.image = capture
        self.timestamp = timestamp if timestamp is not None else int(round(time.time() * 1000))


class ScreenCapturer:
    def __init__(self, x, y, width, height):
        self.region = {"top": y, "left": x, "width": width, "height": height}
        self.sct = None

    def capture(self):
        if self.sct is None:
            self.sct = mss.mss()

        screenshot = self.sct.grab(self.region)
        img_array = np.array(screenshot)
        img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        return Capture(img_rgb)
