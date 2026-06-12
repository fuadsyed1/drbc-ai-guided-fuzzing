import ast
import operator as op

OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def eval_expr(expr):
    node = ast.parse(expr, mode="eval").body
    return eval_node(node)

def eval_node(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        left = eval_node(node.left)
        right = eval_node(node.right)
        return OPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        value = eval_node(node.operand)
        return OPS[type(node.op)](value)

    raise ValueError("Unsupported expression")

if __name__ == "__main__":
    while True:
        try:
            expr = input("Enter expression: ")
            result = eval_expr(expr)
            print(result)

        except Exception as e:
            print(f"ERROR: {e}")