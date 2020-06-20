import sys
import os
import argparse
import time
import datetime
import cv2
import numpy as np
from enum import Enum
from threading import Timer
import pyautogui

from eye_tracker import EyeTracker
from screen import Screen
from quiz import Quiz


class Mode(Enum):
    AWAITING = 0
    READING = 1
    ANSWERING = 2
    BEGINNING = 3
    COMPLETED = 4

RES_SCREEN = pyautogui.size() # RES_SCREEN[0] -> width
                              # RES_SCREEN[1] -> heigth

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 360

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

TIME_READING = 7
TIME_ANSWERING = 5


#TIME_READING = 0.5
#TIME_ANSWERING = 0.5

mode = Mode.BEGINNING

def timeout_reading():
    global mode
    mode = Mode.ANSWERING
    timer_answering = Timer(TIME_ANSWERING, timeout_answering)
    timer_answering.start()
    return

def timeout_answering():
    global mode
    mode = Mode.AWAITING
    return


def nothing():
    pass


def main():
    global mode

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    eye_tracker = EyeTracker()
    screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    screen.clean()
    screen.print_instructions()
    screen.show()

    quiz = None
    cv2.namedWindow("frame")
    cv2.createTrackbar('threshold', 'frame', 0, 255, nothing)
    cv2.setTrackbarPos('threshold', 'frame', 25)

    os.makedirs("./images", exist_ok=True)

    while True:
        print(mode)

        _, frame = camera.read() 
        start = time.time()
        eye_tracker.update(frame)
        end = time.time()
        print("TIME: {:.3f} ms".format(end*1000 - start*1000))

        dec_frame = eye_tracker.decorate_frame()
        dec_frame = cv2.resize(dec_frame,(int(FRAME_WIDTH / 1.5), int(FRAME_HEIGHT / 1.5)))

        cv2.namedWindow("frame")
        cv2.moveWindow("frame", int(RES_SCREEN[0] / 2 - FRAME_WIDTH / 3), screen.height + 75)
        cv2.imshow('frame', dec_frame)


        screen.clean()
        screen.update_frame(dec_frame)
        screen.print_instructions()

        direction = eye_tracker.get_looking_direction()
        print("DIRECTION: {}".format(direction))

        if direction:
            screen.update(direction)
            screen.color_answers()
        else:
            screen.clean_answers()
        screen.show()

        if mode == Mode.READING:
            screen.clean()
            screen.print_instructions()
            screen.print_question(question)
            screen.show()

        if mode == Mode.ANSWERING:
            screen.clean()
            screen.print_instructions()
            screen.print_question(question)
            screen.print_answers()

            direction = eye_tracker.get_looking_direction()
            print("DIRECTION: {}".format(direction))

            if direction:
                screen.update(direction)
                screen.color_answers()
                if direction == 'left':
                    quiz.add_answer(id_q, 'yes')
                if direction == 'right':
                    quiz.add_answer(id_q, 'no')
            else:
                screen.clean_answers()
            screen.show()

        if mode == Mode.AWAITING:
            answer = quiz.get_answer(id_q)
            screen.clean()
            screen.print_instructions()
            screen.print_question(question)
            screen.confirm_answer(answer)
            screen.show()


        if mode == Mode.COMPLETED:
            result = quiz.compute_result()
            screen.clean()
            screen.print_instructions()
            screen.show_result(result)


        k = cv2.waitKey(1) & 0xff

        if k == 1048603 or k == 27: # esc to terminate quiz
            break
        if k == ord('s'): # start quiz
            quiz = Quiz()
            id_q = list(quiz.questions.keys())[0]
            question = quiz.questions.pop(id_q)
            mode = Mode.READING
            timer_reading = Timer(TIME_READING, timeout_reading)
            timer_reading.start()
        if k == ord('n') and mode == Mode.AWAITING: # next question
            # end quiz condition
            if len(quiz.questions.keys()) == 0:
                mode = Mode.COMPLETED
            else:
                id_q = list(quiz.questions.keys())[0]
                question = quiz.questions.pop(id_q)
                mode = Mode.READING
                timer_reading = Timer(TIME_READING, timeout_reading)
                timer_reading.start()


    camera.release()
    cv2.destroyAllWindows()
    os._exit(0)


if __name__ == '__main__':
    main()
