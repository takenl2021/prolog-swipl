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
        self.discontiguous_directives = """\
    :- discontiguous simple_server:surf/3.
    :- discontiguous simple_server:sloc/3.
    :- discontiguous simple_server:morph/3.
    :- discontiguous simple_server:chunk/3.
    :- discontiguous simple_server:dep/3.
    :- discontiguous simple_server:main/3.
    :- discontiguous simple_server:part/3.
    :- discontiguous simple_server:role/3.
    :- discontiguous simple_server:semantic/3.
    :- discontiguous simple_server:surfBF/3.
    :- discontiguous simple_server:pos/3.
    """

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
    
    #1回で解探索するとき 
    def solve_pyswip(self, query):
        prolog = Prolog()
        file_path = f"/usr/app/gen_pl/temp_prolog_db.pl"
        with open(file_path, 'w') as f:
            f.write(self.database)

        prolog.consult(file_path)
        
        answers = list(prolog.query(query))
        
        return answers
     
     #1文ずつ解探索するとき 
    def solve_pyswip2(self, query):
        prolog = Prolog()
        file_path = f"/usr/app/gen_pl/{gen_random_name(10)}.pl"
        #file_path = f"/usr/app/gen_pl/temp_prolog_db.pl"
        with open(file_path, 'w') as f:
            f.write(self.database)

        prolog.consult(file_path)
        print(prolog.query(query))
        answers = list(prolog.query(query))
        #os.remove(file_path)
        return answers


    #　swi-prologサーバをたてて解探索する
    #  djangoが検索処理をマルチスレッドで実行できるようになり，swiplサーバを自由にカスタマイズできるが，
    #  詳細な設定が記載されたdocumnetが少ないため，chatgptで聞いてもうまく調整できなかった
    def solve_pyswip_svr(self, query):
        #　swi-prologは違うファイル名でconsultするとクエリがsyntax errorが発生した際に
        #  前回のファイルの解を返却する謎仕様であるため同名ファイルを読み込ませる
        prolog = PrologInterface()
        file_path = f"/usr/app/gen_pl/temp_prolog_db.pl"
        #file_path = f"/usr/app/gen_pl/{gen_random_name(10)}.pl"

        with open(file_path, 'w') as f:
            #f.write(self.database)
            f.write(f"{self.discontiguous_directives}\n{self.database}")
        prolog.consult(file_path)
    
        answers = prolog.query(query)
        
        #os.remove(file_path)  # ファイル削除
        return answers
