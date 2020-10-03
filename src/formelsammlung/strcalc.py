# noqa: D205,D208,D400
"""
    formelsammlung.strcalc
    ~~~~~~~~~~~~~~~~~~~~~~

    Calculate arithmetic expressions from strings.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
import ast
import operator

from typing import Union, Optional


T_Number = Union[int, float, complex]


class _StringCalculator(ast.NodeVisitor):
    """Calculate an arithmetic expression from a string using :py:mod:`ast`."""

    # pylint: disable=C0103
    def visit_BinOp(self, node: ast.BinOp) -> T_Number:  # noqa: N802
        """Handle `BinOp` nodes."""
        return {
            ast.Add: operator.add,  #: a + b
            ast.Sub: operator.sub,  #: a - b
            ast.Mult: operator.mul,  #: a * b
            ast.Pow: operator.pow,  #: a ** b
            ast.Div: operator.truediv,  #: a / b
            ast.FloorDiv: operator.floordiv,  #: a // b
            ast.Mod: operator.mod,  #: a % b
        }[type(node.op)](self.visit(node.left), self.visit(node.right))

    # fmt: off
    def visit_UnaryOp(self, node: ast.UnaryOp) -> T_Number:  # noqa: N802
        """Handle `UnaryOp` nodes."""
        return {
            ast.UAdd: operator.pos,  #: + a
            ast.USub: operator.neg,  #: - a
        }[type(node.op)](self.visit(node.operand))
    # fmt: on

    def visit_Constant(self, node: ast.Constant) -> T_Number:  # noqa: N802
        """Handle `Constant` nodes."""
        return node.value

    def visit_Num(self, node: ast.Num) -> T_Number:  # noqa: N802
        """Handle `Num` nodes.

        For backwards compatibility <3.8. Since 3.8 ``visit_Constant`` is used.
        """
        return node.n

    def visit_Expr(self, node: ast.Expr) -> T_Number:  # noqa: N802
        """Handle `Expr` nodes."""
        return self.visit(node.value)


def calculate_string(expression: str) -> Optional[T_Number]:
    """Calculate the given expression.

    The given arithmetic expression string is parsed as an :py:mod:`ast` and then
    handled by the :py:class:`ast.NodeVisitor`.

    Python exceptions are risen like with normal arithmetic expression e.g.
    :py:class:`ZeroDivisionError`.

    Supported number types:

        - :py:class:`int` ``1``
        - :py:class:`float` ``1.1``
        - :py:class:`complex` ``1+1j``

    Supported mathematical operators:

        - Positive (:py:func:`operator.pos`) ``+ a``
        - Negative (:py:func:`operator.neg`) ``- a``
        - Addition (:py:func:`operator.add`) ``a + b``
        - Subtraction (:py:func:`operator.sub`) ``a - b``
        - Multiplication (:py:func:`operator.mul`) ``a * b``
        - Exponentiation (:py:func:`operator.pow`) ``a ** b``
        - Division (:py:func:`operator.truediv`) ``a / b``
        - FloorDivision (:py:func:`operator.floordiv`) ``a // b``
        - Modulo (:py:func:`operator.mod`) ``a % b``

    :param expression: String with arithmetic expression.
    :return: Result or None
    """
    if expression == "":
        return None
    return _StringCalculator().visit(ast.parse(expression).body[0])
