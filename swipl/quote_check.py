import re


def optimized_remove_quotes(data):
    for item in data:
        for key, value in item.items():
            if isinstance(value, str):  # 文字列の場合のみ処理
                # 数字_数字の形式かチェック
                if "_" in value and value.startswith("'") and value.endswith("'"):
                    item[key] = value.strip("'")  # 二重引用符を削除
                # 数字のみの形式かチェック
                elif value.isdigit() and value.startswith("'") and value.endswith("'"):
                    item[key] = int(value.strip("'"))  # 一重引用符を削除してint型に変換
                elif value.isdigit():  # 数字形式で一重引用符なし
                    item[key] = int(value)  # int型に変換
    return data


def optimized_quote_japanese_args(prolog_code):
    # Regular expression to find Prolog predicates
    predicate_regex = r"([a-zA-Z_][a-zA-Z0-9_]*\([^()]*\))"
    # Regular expression for Japanese characters
    japanese_char_regex = r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]'

    # Find all predicates
    predicates = re.findall(predicate_regex, prolog_code)
    new_code = prolog_code

    for pred in predicates:
        # Skip re_match predicates
        if pred.startswith('re_match('):
            continue

        # Split predicate into name and args
        name, args = pred.split('(', 1)
        args = args[:-1]  # remove trailing )

        # Process each argument
        quoted_args = []
        for arg in args.split(','):
            # Quote argument if it contains Japanese characters
            if re.search(japanese_char_regex, arg):
                arg = "'" + arg + "'"
            quoted_args.append(arg)

        # Construct the new predicate
        new_pred = name + '(' + ','.join(quoted_args) + ')'

        # Replace old predicate with new in the code
        new_code = new_code.replace(pred, new_pred)

    return new_code