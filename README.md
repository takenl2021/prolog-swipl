# パターンマッチ処理モジュール

このモジュールはdjango-asa2prolog(https://github.com/takenl2021/django-asa2prolog) でパターンマッチ処理を行う際に，SWI-PrologのHTTPサーバとのrequest処理を行うためのライブラリである．


## インストール
このモジュールを使用するには，以下のライブラリが必要です．
- pyswip
- requests
- decouple

```
$ pip install pyswip requests python-decouple
```
## URL指定
本ライブラリを用いて
SWI-PrologのHTTPサーバでパターンマッチを実行するには，各自でSWI-PrologのHTTPサーバを起動し，SWI-PrologのURLを以下のように.envファイルに環境変数を設定することで利用できる
### .envファイル
```
SWI_PROLOG_HOST_API=http://localhost:5000
PROLOG_FILE_PATH=/usr/app/gen_pl
```
django-asa2prolog(https://github.com/takenl2021/django-asa2prolog) のプロジェクトの場合はexample.envに設定する．
## 使用例
```
### 初期設定 ###
## prolog知識データベース
knowledge = """
parent(john, jim).
parent(john, ann).
parent(jim, bob).
"""
## クエリのルール
rules = """
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
"""
## 検索クエリ
query= grandparent(X, Z)

### 実装時 ####
##　メソッドにprologデータと検索クエリを初期化
processor = Processor(knowledge, rules)
# pyswipを使用してクエリを解決
result = processor.solve_pyswip("grandparent(john, X)")
print(result)

# SWI-Prologサーバーを使用してクエリを解決
result = processor.solve_pyswip_svr("grandparent(john, X)")
print(result)
```

## 注意点
Docker環境で構築したため，ローカル環境での動作保証できない．

基本的には**solve_pyswip_svr**メソッドを利用すべきであるが，SWI-Prologサーバーが起動できない場合は
**solve_pyswip_svr**メソッドを用いてもよいが，警告表示が行われるため，処理時間がかなり低下する．
django-asa2prolog(https://github.com/takenl2021/django-asa2prolog)のプロジェクトを使わずに，

