import re


def quote_japanese_in_args(prolog_code):
    # Regular expression to find Prolog predicates
    regex = r"([a-zA-Z_][a-zA-Z0-9_]*\([^()]*\))"

    # Find all predicates
    predicates = re.findall(regex, prolog_code)

    for pred in predicates:
        # Split predicate into name and args
        name, args = pred.split('(')
        args = args[:-1]  # remove trailing )
        args = args.split(',')

        # Check each argument if it contains any Japanese character
        for i, arg in enumerate(args):
            if re.search(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]', arg):
                # Surround with single quotes
                args[i] = "'" + arg + "'"

        # Join arguments back and form the full predicate
        new_pred = name + '(' + ','.join(args) + ')'

        # Replace old predicate with new in the code
        prolog_code = prolog_code.replace(pred, new_pred)

    return prolog_code
