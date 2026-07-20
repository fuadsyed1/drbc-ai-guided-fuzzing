import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_eval_expression(expression):
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as error:
        raise SyntaxError(f"Invalid arithmetic expression: {error}")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            return OPERATORS[type(node.op)](left, right)

        raise ValueError("Unsupported arithmetic expression")

    return evaluate(tree)


def process_input(input_string):
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")

    if not input_string.strip():
        raise ValueError("Arithmetic script cannot be empty")

    statements = [part.strip() for part in input_string.split(";") if part.strip()]

    if not statements:
        raise ValueError("No script statements found")

    variables = {}
    outputs = []

    for statement in statements:
        if statement.startswith("LET "):
            body = statement[4:].strip()

            if "=" not in body:
                raise ValueError("LET statement must contain =")

            name, expression = body.split("=", 1)
            name = name.strip()
            expression = expression.strip()

            if not name.isidentifier():
                raise ValueError("Invalid variable name")

            value = safe_eval_expression(expression)
            variables[name] = value

        elif statement.startswith("PRINT "):
            name = statement[6:].strip()

            if name not in variables:
                raise KeyError("PRINT references unknown variable")

            outputs.append(variables[name])

        else:
            raise ValueError("Unknown script statement")

    return {
        "valid": True,
        "variables": variables,
        "outputs": outputs,
        "statement_count": len(statements),
    }