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
        self.answers = {id_q: list() for id_q in range(0,13) }
        self.scores = {}
        self.results = None
        self.load_questions()


    def load_questions(self):
        self.questions = {

                  0 : "Would you play\nQuidditch at Hogwarts?",                  # Y>G N>C
                  1 : "Would you excell in Defense\nAgainst the Dark Arts?",     # Y>G N>T
                  2 : "Would you ever go exploring\nin the Forbidden Forest?",   # Y>G N>S
                  3 : "Are you good at\nplaying Wizard's Chess?",                # Y>G N>S

                  4 : "Do you prefer the books\nover the movies?",               # Y>C N>G
                  5 : "Have you ever been laughed\nat school?",                  # Y>C N>T
                  6 : "Is Harry actually a good wizard?",                        # Y>C N>S

                  7 : "Would you want to use\na Portkey?",                       # Y>T N>C
                  8 : "Would you ever want to work\nat the Ministry of Magic?",  # Y>T N>G
                  9 : "Would you have a pet\nwhile at Hogwarts?",                # Y>T N>S

                 10 : "Is Moaning Myrtle annoying?",                             # Y>S N>C
                 11 : "Would you ever call\nsomeone Half-blood?",                 # Y>S N>T
                 12 : "Whould you want to have\nthe Elder Wand?",                # Y>S N>G

            }

        l = list(self.questions.items())
        random.shuffle(l)
        self.questions = dict(l)

        self.scores = {

                  0 : {'yes': 'Gryffindor', 'no': 'Ravenclaw'},  # Y>G N>C
                  1 : {'yes': 'Gryffindor', 'no': 'Hufflepuff'}, # Y>G N>T
                  2 : {'yes': 'Gryffindor', 'no': 'Slytherin'},  # Y>G N>S
                  3 : {'yes': 'Gryffindor', 'no': 'Slytherin'},  # Y>G N>S

                  4 : {'yes': 'Ravenclaw', 'no': 'Gryffindor'},  # Y>C N>G
                  5 : {'yes': 'Ravenclaw', 'no': 'Hufflepuff'},  # Y>C N>T
                  6 : {'yes': 'Ravenclaw', 'no': 'Slytherin'},   # Y>C N>S

                  7 : {'yes': 'Hufflepuff', 'no': 'Ravenclaw'},  # Y>T N>C
                  8 : {'yes': 'Hufflepuff', 'no': 'Gryffindor'}, # Y>T N>G
                  9 : {'yes': 'Hufflepuff', 'no': 'Slytherin'},  # Y>T N>S

                 10 : {'yes': 'Slytherin', 'no': 'Ravenclaw'},   # Y>S N>C
                 11 : {'yes': 'Slytherin', 'no': 'Hufflepuff'},  # Y>S N>T
                 12 : {'yes': 'Slytherin', 'no': 'Gryffindor'},  # Y>S N>G

            }


    def add_answer(self, id_q, answer):
        self.answers[id_q] = self.answers.get(id_q, list())
        self.answers[id_q].append(answer)

    def get_answer(self, id_q):
        answers = self.answers.get(id_q, list())
        num_yes = answers.count('yes') 
        num_no = answers.count('no') 

        if num_yes >= num_no:
            return 'yes'
        elif num_yes < num_no:
            return 'no'
#        else:
#            return random.choice(['yes', 'no'])

    def compute_result(self):
        if self.results == None:
            self.results = {"Gryffindor": 0, "Hufflepuff": 0, "Ravenclaw": 0, "Slytherin": 0 }
            for id_q in self.answers.keys():
                answer = self.get_answer(id_q)
                if answer == 'yes' or answer == 'no':
                    self.results[self.scores[id_q][answer]] += 1

        return max(self.results, key=self.results.get)




