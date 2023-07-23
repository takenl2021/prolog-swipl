import requests
import json


class PrologInterface:
    def __init__(self):
        self.server_url = 'http://localhost:8080/json'
        self.headers = {'content-type': 'application/json'}

    def consult(self, file):
        data = json.dumps({'query': f'consult(\'{file}\')'})
        response = requests.post(
            self.server_url, data=data, headers=self.headers)
        return response.json()

    def query(self, query):
        data = json.dumps({'query': query})
        response = requests.post(
            self.server_url, data=data, headers=self.headers)
        query_response = response.json()

        if query_response['success']:
            var_lists = query_response['vars']
            sol = {item['var']: item['value'] for item in var_lists}
            return sol
        else:
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
