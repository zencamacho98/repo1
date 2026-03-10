from __future__ import annotations

import ast
import operator as op
from typing import Any


# --- Safe evaluation helpers ---

# Supported binary operators
_ALLOWED_OPERATORS: dict[type[ast.AST], Any] = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Supported unary operators
_ALLOWED_UNARY_OPERATORS: dict[type[ast.AST], Any] = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def _eval_node(node: ast.AST) -> float:
    """Recursively evaluate a restricted AST node."""

    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Only numeric constants are allowed")

    if isinstance(node, ast.BinOp):
        if type(node.op) not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        if type(node.op) not in _ALLOWED_UNARY_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        operand = _eval_node(node.operand)
        return _ALLOWED_UNARY_OPERATORS[type(node.op)](operand)

    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def evaluate_expression(expr: str) -> float:
    """Safely evaluate a simple math expression.

    This intentionally avoids Python's built-in `eval` to prevent arbitrary
    code execution. Only numeric literals and a small set of operators are
    allowed.
    """

    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid expression") from exc

    return _eval_node(parsed)  # type: ignore[arg-type]
