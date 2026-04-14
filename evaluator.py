# ---------- TOKENIZER ---------- #
def tokenize(expr):
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch.isdigit():
            num = ch
            i += 1
            while i < len(expr) and expr[i].isdigit():
                num += expr[i]
                i += 1
            tokens.append(("NUM", int(num)))
            continue

        elif ch in "+-*/":
            tokens.append(("OP", ch))

        elif ch == "(":
            tokens.append(("LPAREN", ch))

        elif ch == ")":
            tokens.append(("RPAREN", ch))

        elif ch == " ":
            pass
        else:
            raise Exception("Invalid character")

        i += 1

    tokens.append(("END", ""))
    return tokens


# ---------- GLOBAL POINTER ---------- #
tokens = []
pos = 0

def current():
    return tokens[pos]

def eat():
    global pos
    pos += 1


# ---------- PARSER ---------- #
def parse_expression():
    node = parse_term()

    while current()[0] == "OP" and current()[1] in "+-":
        op = current()[1]
        eat()
        right = parse_term()
        node = (op, node, right)

    return node


def parse_term():
    node = parse_factor()

    while current()[0] == "OP" and current()[1] in "*/":
        op = current()[1]
        eat()
        right = parse_factor()
        node = (op, node, right)

    return node


def parse_factor():
    token = current()

    # unary negation
    if token[0] == "OP" and token[1] == "-":
        eat()
        return ("neg", parse_factor())

    # number
    if token[0] == "NUM":
        eat()
        node = token[1]

        # implicit multiplication: 3(4+5)
        if current()[0] == "LPAREN":
            right = parse_factor()
            return ("*", node, right)

        return node

    # parentheses
    if token[0] == "LPAREN":
        eat()
        node = parse_expression()

        if current()[0] != "RPAREN":
            raise Exception("Missing )")

        eat()

        # implicit multiplication: (2+3)4
        if current()[0] == "NUM":
            right = parse_factor()
            return ("*", node, right)

        return node

    raise Exception("Invalid syntax")


# ---------- TREE STRING ---------- #
def tree_to_string(node):
    if isinstance(node, int):
        return str(node)

    if node[0] == "neg":
        return f"(neg {tree_to_string(node[1])})"

    return f"({node[0]} {tree_to_string(node[1])} {tree_to_string(node[2])})"


# ---------- EVALUATE ---------- #
def evaluate(node):
    if isinstance(node, int):
        return node

    if node[0] == "+":
        return evaluate(node[1]) + evaluate(node[2])

    if node[0] == "-":
        return evaluate(node[1]) - evaluate(node[2])

    if node[0] == "*":
        return evaluate(node[1]) * evaluate(node[2])

    if node[0] == "/":
        return evaluate(node[1]) / evaluate(node[2])

    if node[0] == "neg":
        return -evaluate(node[1])


# ---------- TOKEN STRING ---------- #
def tokens_to_string(tokens):
    result = []
    for t in tokens:
        if t[0] == "END":
            result.append("[END]")
        else:
            result.append(f"[{t[0]}:{t[1]}]")
    return " ".join(result)


# ---------- MAIN FUNCTION ---------- #
def evaluate_file(input_path):
    results = []

    with open(input_path, "r") as f:
        lines = f.readlines()

    global tokens, pos

    for line in lines:
        expr = line.strip()

        try:
            tokens = tokenize(expr)
            pos = 0

            tree = parse_expression()

            if current()[0] != "END":
                raise Exception()

            tree_str = tree_to_string(tree)
            result = evaluate(tree)

            # format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 4)

            tokens_str = tokens_to_string(tokens)

        except:
            tree_str = "ERROR"
            tokens_str = "ERROR"
            result = "ERROR"

        results.append({
            "input": expr,
            "tree": tree_str,
            "tokens": tokens_str,
            "result": result
        })

    # write output file
    with open("output.txt", "w") as f:
        for r in results:
            f.write(f"Input: {r['input']}\n")
            f.write(f"Tree: {r['tree']}\n")
            f.write(f"Tokens: {r['tokens']}\n")
            f.write(f"Result: {r['result']}\n\n")

    return results


# ---------- RUN ---------- #
if __name__ == "__main__":
    evaluate_file("sample_input.txt")