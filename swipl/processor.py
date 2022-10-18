from prologpy.solver import Solver
import pytholog
from pyswip import Prolog
import numpy as np
import random
import string

def gen_random_name(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

class Processor():
    def __init__(self, knowledge, rules):
        self.database = knowledge + '\n' + rules

    def solve_prologpy(self, query):
        prolog = Solver(self.database)
        solutions = dict(prolog.find_solutions(query))
        try:
            transposed = np.array([solutions[key] for key in solutions.keys()]).T
            answers = []
            for t in transposed:
                answer = {}
                for key, value in zip(solutions.keys(), t):
                    answer[key] = value
                answers.append(answer)
            return answers
        except:
            return None
    
    def solve_pytholog(self, query):
        prolog = pytholog.KnowledgeBase("demo")
        prolog(self.database.replace(".","").split("\n"))
        answers = prolog.query(pytholog.Expr(query))
        return answers
    
    def solve_pyswip(self, query):
        prolog = Prolog()
        file_path = f"{gen_random_name(10)}.pl"
        with open(file_path, 'w') as f:
            f.write(self.database)
        prolog.consult(file_path)
        answers = list(prolog.query(query))
        return answers
