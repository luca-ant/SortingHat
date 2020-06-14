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
        self.current_answer = None
        self.screen = np.ones((self.height, self.width, 3))
        self.print_instructions()
        self.frame = np.zeros((720, self.width, 3))

    def clean_answers(self):
        cv2.rectangle(self.screen, (0,self.height // 3), (self.width, self.height), (255,255,255), -1)
        self.print_answers()

    def color_answers(self):
        cv2.rectangle(self.screen, (0,self.height // 3), (self.width, self.height), (255,255,255), -1)
        if self.current_answer == 'yes':
            cv2.rectangle(self.screen, (0, self.height // 3), (self.width // 2, self.height), (0,0,255), -1)

        if self.current_answer == 'no':
            cv2.rectangle(self.screen, (self.width // 2, self.height // 3), (self.width, self.height), (0,0,255), -1)
        self.print_answers()

    def confirm_answer(self, answer):
        cv2.rectangle(self.screen, (0,self.height // 3), (self.width, self.height), (255,255,255), -1)
        if answer == 'yes':
            cv2.rectangle(self.screen, (0, self.height // 3), (self.width // 2, self.height), (0,255,0), -1)

        if answer == 'no':
            cv2.rectangle(self.screen, (self.width // 2, self.height // 3), (self.width, self.height), (0,255,0), -1)
        self.print_answers()

    def update_frame(self, frame):
        self.frame = frame

    def update(self, direction):
        if direction == 'left':
            self.current_answer = 'yes'
        if direction == 'right':
            self.current_answer = 'no'

    def clean(self):
        self.screen = np.ones((self.height, self.width, 3))

#    def update_time(self, progress=0):
#        x, y = (int)
#        if progress == 1.0:
#            cv2.circle(self.screen, (x, y), 5, (0, 255, 0), -1)
#        else:
#            cv2.circle(self.screen, (x, y), 5, (0, 0, 0), -1)
#
#        if progress > 0:
#            # Ellipse parameters
#            radius = 20
#            axes = (radius, radius)
#            angle = 0
#            start_angle = 0
#            end_angle = 360 * progress
#            cv2.ellipse(self.screen, (x, y), axes, angle, start_angle, end_angle, (0, 255, 0), 2)



    def print_answers(self):

        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 2
        th = 3

        answer = 'Look left\nfor YES'

        for i, line in enumerate(answer.split('\n')):
            textsize = cv2.getTextSize(line, font, fs, th)[0]
            x = (self.width // 2 - textsize[0]) // 2
            y0, dy = self.height // 3 + ((2 * (self.height // 3) + textsize[1]) // 2) - textsize[1], textsize[1] + 30
            y = y0 + i*dy
            cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)

        answer = 'Look right\nfor NO'

        for i, line in enumerate(answer.split('\n')):
            textsize = cv2.getTextSize(line, font, fs, th)[0]
            x = self.width // 2 + (self.width // 2 - textsize[0]) // 2
            y0, dy = self.height // 3 + ((2 * (self.height // 3) + textsize[1]) // 2) - textsize[1], textsize[1] + 30
            y = y0 + i*dy
            cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)

#        font = cv2.FONT_HERSHEY_SIMPLEX
#        fs = 5
#        th = 5
#
#        line = 'Look left for YES'
#        textsize = cv2.getTextSize(line, font, fs, th)[0]
#        x = (self.width // 2 - textsize[0]) // 2
#        y = self.height // 3 + ((2 * (self.height // 3) + textsize[1]) // 2)
#        cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)
#
#        line = 'NO'
#        textsize = cv2.getTextSize(line, font, fs, th)[0]
#        x = self.width // 2 + (self.width // 2 - textsize[0]) // 2
#        y = self.height // 3 + ((2 * (self.height // 3) + textsize[1]) // 2)
#        cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=5, color=(0,0,0), thickness=5)


    def print_question(self, question):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 1
        th = 2
        
        y0, dy = int(0.1 * self.height), 30

        for i, line in enumerate(question.split('\n')):
            textsize = cv2.getTextSize(line, font, fs, th)[0]
            x = self.width // 4 + (self.width // 2 - textsize[0]) // 2
            y = y0 + i*dy
            cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)


    def print_instructions(self):

        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 0.7
        th = 2
        x, y0, dy = int(0.03 * self.width), int(0.07 * self.height), 25

        instructions = "Press:\nESC to quit\ns to start quiz\nn to next question"

        for i, line in enumerate(instructions.split('\n')):
            y = y0 + i*dy
            cv2.putText(img=self.screen, text=line, org=(x, y), fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)

    def show_result(self, result):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 1
        th = 2
        line = 'You are assigned to...'
        textsize = cv2.getTextSize(line, font, fs, th)[0]
        x = self.width // 4 + (self.width // 2 - textsize[0]) // 2
        y = int(0.1 * self.height) + textsize[1]
        cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)

        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 2
        th = 3
        line = result.upper()
        textsize = cv2.getTextSize(line, font, fs, th)[0]
        x = (self.width - textsize[0]) // 2
        y = int(0.9 * self.height) - textsize[1]
        cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)
        self.show()

    def show(self):
        cv2.namedWindow("screen")
#        cv2.moveWindow("screen", int(960 - self.width/2), 0)
        cv2.moveWindow("screen", 0, 0)

#        cv2.namedWindow("screen", cv2.WND_PROP_FULLSCREEN)
#        cv2.setWindowProperty("screen",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("screen", self.screen)

#        to_show = cv2.vconcat([self.screen.astype(np.uint8), self.frame.astype(np.uint8)])
#        cv2.imshow("screen", to_show)



