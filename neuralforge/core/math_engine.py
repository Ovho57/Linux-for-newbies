"""Safe mathematical expression evaluation and educational traces."""
import ast
import math
import operator

_ALLOWED_BINARY = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
}
_ALLOWED_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_ALLOWED_FUNCTIONS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
    "exp": math.exp, "abs": abs,
}
_ALLOWED_CONSTANTS = {"pi": math.pi, "e": math.e}


def safe_evaluate(expression: str, variables: dict[str, float] | None = None) -> float:
    """Evaluate a small mathematical grammar. Never executes arbitrary Python."""
    variables = variables or {}
    tree = ast.parse(expression, mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.Name):
            if node.id in variables:
                return float(variables[node.id])
            if node.id in _ALLOWED_CONSTANTS:
                return _ALLOWED_CONSTANTS[node.id]
            raise ValueError(f"Unknown symbol: {node.id}")
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINARY:
            return _ALLOWED_BINARY[type(node.op)](visit(node.left), visit(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
            return _ALLOWED_UNARY[type(node.op)](visit(node.operand))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _ALLOWED_FUNCTIONS:
            if node.keywords:
                raise ValueError("Keyword arguments are not supported.")
            return _ALLOWED_FUNCTIONS[node.func.id](*(visit(arg) for arg in node.args))
        raise ValueError("Unsupported expression. Use arithmetic, pi, e and supported math functions.")

    result = float(visit(tree))
    if not math.isfinite(result):
        raise ValueError("The result is not finite.")
    return result


def weighted_sum_trace(weights: list[float], inputs: list[float], bias: float) -> dict:
    if len(weights) != len(inputs):
        raise ValueError("Weights and inputs must have the same length.")
    terms = [{"weight": float(w), "input": float(x), "product": float(w * x)}
             for w, x in zip(weights, inputs)]
    total = sum(item["product"] for item in terms) + float(bias)
    return {"terms": terms, "bias": float(bias), "z": float(total)}
