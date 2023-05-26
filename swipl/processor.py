from prologpy.solver import Solver
import pytholog
from pyswip import Prolog
# from pyswip_alt import Prolog
import numpy as np
import random
import string
from time import sleep
import os
import re
from pyswip import Prolog
from .quote_check import quote_japanese_in_args


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
        file_path = f"/home/katsura/kenkyu/B4/django-asa2prolog/gen_pl/{gen_random_name(10)}.pl"
        pl_data = quote_japanese_in_args(self.database)
        print(pl_data)
        with open(file_path, 'w') as f:
            # f.write(self.database)
            f.write(pl_data)  # pldataは

        prolog.consult(file_path)
        answers = list(prolog.query(query))
        os.remove(file_path)  # ファイル削除
        return answers

    def solve_pyswip_assert(self, query):
        prolog = Prolog()

        segments = self.database.replace(".", " ").split("\n")
        """
        file_path = f"/home/katsura/kenkyu/B4/django-asa2prolog/gen_pl/{gen_random_name(10)}.pl"
        with open(file_path, 'w') as f:
            f.write(self.rules)
        
        # 第3要素が空のときもしくは"・"もしくは"/"が含まれるとき
        # シングルクオーテーションを付与する関数 ex)semantic(0,3,生成・消滅)  =>semantic(0,3,'生成・消滅')

        def add_single_quotes_if_needed(text):
            def repl(match):
                arg = match.group(2)
                if arg == '' or '・' in arg or '／' in arg or ' ' in arg:
                    return f"{match.group(1)}'{arg}'{match.group(3)}"
                else:
                    return match.group(0)

            pattern = r'(\w+\([^\),]*,[^\),]*,\s*)([^,\)]*)(\s*\))'
            return re.sub(pattern, repl, text)
        """

        # assertで1つずつ追加

        for segment in segments:
            #segment = add_single_quotes_if_needed(segment)
            segment = quote_japanese_in_args(segment)
            print(segment)

            prolog.assertz(segment)

        print("Waiting Match....")

        answers = list(prolog.query(query))

        # 再定義されてしまうので追加した定義をすべて削除
        for segment in segments:
            segment = quote_japanese_in_args(segment)
            # print(segment)
            prolog.retract(segment)

        # os.remove(file_path)  # ファイル削除
        return answers
