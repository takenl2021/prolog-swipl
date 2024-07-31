from prologpy.solver import Solver
import pytholog
from pyswip import Prolog
import numpy as np
import random
import string
import os
from pyswip import Prolog
from .quote_check import quote_japanese_in_args
from .pyswip_svr import PrologInterface


def gen_random_name(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class Processor():
    def __init__(self, knowledge, rules):
        self.database = knowledge + '\n' + rules

    def solve_prologpy(self, query):
        prolog = Solver(self.database)
        solutions = dict(prolog.find_solutions(query))
        try:
            transposed = np.array([solutions[key]
                                  for key in solutions.keys()]).T
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
        prolog(self.database.replace(".", "").split("\n"))
        answers = prolog.query(pytholog.Expr(query))
        return answers

    def solve_pyswip(self, query):
        prolog = Prolog()
        file_path = f"/usr/app/gen_pl/temp_prolog_db..pl"

        with open(file_path, 'w') as f:
            f.write(self.database)
           

        prolog.consult(file_path)
        answers = list(prolog.query(query))
        os.remove(file_path)  # ファイル削除
        return answers



    def solve_pyswip_svr(self, query):
        prolog = PrologInterface()
        file_path = f"/home/katsura/kenkyu/B4/django-asa2prolog/gen_pl/{gen_random_name(10)}.pl"
        pl_data = quote_japanese_in_args(self.database)
        with open(file_path, 'w') as f:
            # f.write(self.database)
            f.write(pl_data)  # pldataは

        prolog.consult(file_path)
        answers = prolog.query(query)
        os.remove(file_path)  # ファイル削除
        return answers
