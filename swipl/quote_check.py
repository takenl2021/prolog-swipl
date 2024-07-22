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