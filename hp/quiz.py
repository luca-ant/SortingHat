import numpy as np
import cv2
import random

class Quiz:
    """
    Class for quiz data
    Attributes:
        width: screen width in pixels
        height: screnn height in pixels
        pointer: coordinates (x, y) of pointer position in pixels
    Methods:
    """
    def __init__(self):
        self.questions = {}
        self.answers = {}
        self.output = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]
        self.load_questions()


    def load_questions(self):
        self.questions = {
                        0 : "Prima\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\nasdasdadadasd\n",
                        1 : "Seconda",
                        2 : "Terza"
                    }

        l = list(self.questions.items())
        random.shuffle(l)
        self.questions = dict(l)

    def add_answer(self, id_q, answer):
        self.answers[id_q] = self.answers.get(id_q, list())
        self.answers[id_q].append(answer)
        print(self.answers)
    
    def get_answer(self, id_q):
        answers = self.answers.get(id_q, list())
        num_yes = answers.count('yes') 
        num_no = answers.count('no') 

        if num_yes >= num_no:
            return 'yes'
        else:
            return 'no'


    def compute_result(self):

        return self.output[0]




