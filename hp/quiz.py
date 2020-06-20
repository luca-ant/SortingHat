import numpy as np
import cv2
import random

class Quiz:
    """
    Class for quiz data
    Attributes:
        questions: a dictionary contains all questions (id: string)
        answers: a dictionary contains all the user answers (id: list of answers)
        results: a dictionary contains the final computed result of the quiz (string: score)
    """
    def __init__(self):
        self.questions = {}
        self.answers = {}
        self.results = {"Gryffindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0 }
        self.load_questions()


    def load_questions(self):
        self.questions = {
                        0 : "Would you play\nQuidditch at Hogwarts?",
                        1 : "Would you excell in Defense\nAgainst the Dark Arts?",
                        2 : "Are you good at\nplaying Wizard's Chess?",
                        3 : "You catch a classmate cheating\non their exams. Do you tell them?",
                        4 : "Would you ever receive a\nHowler from your parents?",
                        5 : "Would you have a pet\nwhile at Hogwarts?",
                        6 : "Would you ever go exploring\nin the Forbidden Forest?",
                        7 : "Would you ever want to work\nat the Ministry of Magic?",
                        8 : "Whould you want to have\nthe Elder Wand?",
                        9 : "Would you ever go snooping in the\nforbidden section of the library?",
                        10 : "Is Moaning Myrtle annoying?",
                        11 : "Would you ever participate in a duel?",
                        12 : "Is Harry actually a good wizard?",
                        13 : "Do you prefer the books over the movies?",
                        14 : "",
                        15 : ""
                    }

        l = list(self.questions.items())
        random.shuffle(l)
        self.questions = dict(l)

    def add_answer(self, id_q, answer):
        self.answers[id_q] = self.answers.get(id_q, list())
        self.answers[id_q].append(answer)

    def get_answer(self, id_q):
        answers = self.answers.get(id_q, list())
        num_yes = answers.count('yes') 
        num_no = answers.count('no') 

        if num_yes >= num_no:
            return 'yes'
        else:
            return 'no'

    def compute_result(self):

        self.results = {"Gryffindor": 4, "Hufflepuff": 5, "Ravenclaw": 0, "Slytherin": 0 }

        return max(self.results, key=self.results.get)




