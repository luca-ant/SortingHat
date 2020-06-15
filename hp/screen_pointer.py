import numpy as np
import cv2

class Screen:
    """
    Class for a fake screen
    Attributes:
        width: screen width in pixels
        height: screnn height in pixels
        pointer: coordinates (x, y) of pointer position in pixels
    Methods:
    """
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.pointer = (0,0)
        self.mode = "normal"
        self.screen = np.ones((self.height, self.width, 3))
        self.clean()

    def refresh(self):
        self.clean()
        self.draw_pointer()
        self.show()

    def update(self, gaze):
        self.pointer = gaze

    def clean(self):
        self.screen = np.ones((self.height, self.width, 3))
        self.print_instructions()

    def draw(self, point, progress=0):
        x, y = point
        if progress == 1.0:
            cv2.circle(self.screen, (x, y), 5, (0, 255, 0), -1)
        else:
            cv2.circle(self.screen, (x, y), 5, (0, 0, 0), -1)

        if progress > 0:
            # Ellipse parameters
            radius = 7
            axes = (radius, radius)
            angle = 0
            start_angle = 0
            end_angle = 360 * progress
            cv2.ellipse(self.screen, (x, y), axes, angle, start_angle, end_angle, (0, 255, 0), 2)


    def draw_center(self):
        x, y = (int(0.5 * self.width), int(0.5 * self.height))
        cv2.circle(self.screen, (x, y), 5, (0, 0, 0), -1)

    def draw_pointer(self):
        x, y = self.pointer
        cv2.circle(self.screen, (x, y), 5, (0, 255, 0), -1)

    def print_instructions(self):
        x, y0, dy = int(0.03 * self.width), int(0.8 * self.height), 35

        if self.mode == "normal":
            instructions = "Press:\nESC to quit\nc to start calibration"
        if self.mode == "calibration":
            instructions = "Press:\nESC to terminate\nn to next calibration step"

        for i, line in enumerate(instructions.split('\n')):
            y = y0 + i*dy
            cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, color=(0,0,0), thickness=2)


    def show(self):
        cv2.namedWindow("screen")
#        cv2.moveWindow("screen", int(960 - self.width/2), 0)

#        cv2.namedWindow("screen", cv2.WND_PROP_FULLSCREEN)
#        cv2.setWindowProperty("screen",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("screen", self.screen)
