import ast
import operator
from collections.abc import Callable

BinaryOperator = Callable[[float, float], float]
UnaryOperator = Callable[[float], float]

# The tool allows only approved arithmetic operations
# A dictionary whose:
#    keys are AST node classes
#    values are BinaryOperator or UnaryOperator objects/functions
OPERATORS: dict[type[ast.AST], BinaryOperator | UnaryOperator] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> float:
    """
    Safely evaluate a basic arithmetic expression.

    Supported operators:
    +, -, *, /, %, ** and parentheses.
    """

    if not expression or not expression.strip():
        raise ValueError("Expression cannot be empty.")

    parsed = ast.parse(expression, mode="eval")
    return _evaluate(parsed.body)


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return node.value

    if isinstance(node, ast.BinOp):
        operator_function = OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported binary operator.")

        return operator_function(
            _evaluate(node.left),
            _evaluate(node.right),
        )

    if isinstance(node, ast.UnaryOp):
        operator_function = OPERATORS.get(type(node.op))

        if operator_function is None:
            raise ValueError("Unsupported unary operator.")

        return operator_function(_evaluate(node.operand))

    raise ValueError("Unsupported mathematical expression.")
