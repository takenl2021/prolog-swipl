import requests
import json


class PrologInterface:
    def __init__(self):
        self.server_url = 'http://montecarlo:5000/json'
        self.headers = {'content-type': 'application/json'}

    # 指定したファイルを読む(prologファイルはテキスト1文ごとに生成)
    def consult(self, file):
        data = json.dumps({'query': f'consult(\'{file}\')'})
        response = requests.post(
            self.server_url, data=data, headers=self.headers)
        return response.json()

    # 解を生成
    def query(self, query):
        data = json.dumps({'query': query})
        response = requests.post(
            self.server_url, data=data, headers=self.headers)
        query_response = response.json()

        if query_response['success']:  # 解が見つかったとき
            var_lists = query_response['vars']
            solution = []
            for var_list in var_lists:  # 複数の解を追加処理
                sol = {item['var']: item['value'] for item in var_list}
                solution.append(sol)
            return solution

        else:  # 解がないとき
            return []


if __name__ == "__main__":
    query = '著者(SENTENCE_ID,Work,WorkSloc,Auth,AuthSloc)'  # 問い合わせるクエリ
    file = 'test2.pl'  # 読むファイル

    # クラスをインスタンス化
    prolog = PrologInterface()

    # 'consult'メソッドを使用
    file_response = prolog.consult(file)

    # 'query'メソッドを使用
    result = prolog.query(query)
    print(result)
