import json
from rules import expressions


def parse_operator(expr):
    opr = expr["operator"]
    left_side = parse(expr["left_side"])
    right_side = parse(expr["right_side"])
    return expressions.Operator(opr, left_side, right_side)


def parse_context_ref(expr):
    name = expr["name"]
    default = expr.get("default", None)
    return expressions.ContextReference(name, default)


def parse_constant(expr):
    return expressions.Constant(expr)


def parse_expr(expr):
    parse_map = {
        "operator": parse_operator,
        "context reference": parse_context_ref,
        "constant": parse_constant,
    }

    if isinstance(expr, list):
        return None  # TODO

    if isinstance(expr, (str, bool, int, float)):
        return expressions.Constant(expr)

    if not isinstance(expr, dict):
        return None

    if "type" not in expr:
        return expressions.Constant(expr)

    expr_type = expr["type"]
    return parse_map[expr_type](expr)


def parse(expr):
    if isinstance(expr, str):
        return parse_expr(json.loads(expr))
    return parse_expr(expr)
