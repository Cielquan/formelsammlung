"""Tests for `strcalc` module."""
import random
from typing import Union

import pytest

from formelsammlung.strcalc import NumberType, StringCalculatorError, calculate_string


def _rand_int_w_0() -> int:
    """Return random positive integer."""
    return random.randrange(100)  # noqa: S311


def _rand_int_wo_0() -> int:
    """Return random positive integer without zero."""
    return random.randrange(1, 100)  # noqa: S311


def _rand_float_w_0() -> float:
    """Return random positive float."""
    return random.uniform(0, 100)  # noqa: S311


def _rand_float_wo_0() -> float:
    """Return random positive float without zero."""
    return random.uniform(1, 100)  # noqa: S311


def _rand_complex_w_0() -> complex:
    """Return random positive complex number.

    The number is made of int for real and imaginary part.
    The imaginary part is randomly positive or negative.
    """
    return complex(f"{_rand_int_w_0()}{random.choice(('+', '-'))}{_rand_int_w_0()}j")  # noqa: S311


def _rand_complex_wo_0() -> complex:
    """Return random positive complex number without zero.

    The number is made of integers for real and imaginary part.
    The imaginary part is randomly positive or negative.
    """
    return complex(
        f"{_rand_int_wo_0()}"  # noqa: S311
        f"{random.choice(('+', '-'))}{_rand_int_wo_0()}j"  # noqa: S311
    )


# Addition


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_addition(num_l: NumberType, num_r: NumberType) -> None:
    """Test addition with calculate_string w/o signs."""
    result = calculate_string(f"{num_l}+{num_r}")

    assert result == num_l + num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_addition_minus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test addition with calculate_string.

    Sign left number: minus
    Sign right number: plus
    """
    result = calculate_string(f"-{num_l}++{num_r}")

    assert result == -num_l + +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_addition_plus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test addition with calculate_string.

    Sign left number: plus
    Sign right number: minus
    """
    result = calculate_string(f"+{num_l}+-{num_r}")

    assert result == +num_l + -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_addition_minus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test addition with calculate_string.

    Sign left number: minus
    Sign right number: minus
    """
    result = calculate_string(f"-{num_l}+-{num_r}")

    assert result == -num_l + -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_addition_plus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test addition with calculate_string.

    Sign left number: plus
    Sign right number: plus
    """
    result = calculate_string(f"+{num_l}++{num_r}")

    assert result == +num_l + +num_r


# Subtraction


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_subtraction(num_l: NumberType, num_r: NumberType) -> None:
    """Test subtraction with calculate_string w/o signs."""
    result = calculate_string(f"{num_l}-{num_r}")

    assert result == num_l - num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_subtraction_minus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test subtraction with calculate_string.

    Sign left number: minus
    Sign right number: plus
    """
    result = calculate_string(f"-{num_l}-+{num_r}")

    assert result == -num_l - +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_subtraction_plus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test subtraction with calculate_string.

    Sign left number: plus
    Sign right number: minus
    """
    result = calculate_string(f"+{num_l}--{num_r}")

    assert result == +num_l - -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_subtraction_minus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test subtraction with calculate_string.

    Sign left number: minus
    Sign right number: minus
    """
    result = calculate_string(f"-{num_l}--{num_r}")

    assert result == -num_l - -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_subtraction_plus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test subtraction with calculate_string.

    Sign left number: plus
    Sign right number: plus
    """
    result = calculate_string(f"+{num_l}-+{num_r}")

    assert result == +num_l - +num_r


# Multiplication


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_multiplication(num_l: NumberType, num_r: NumberType) -> None:
    """Test multiplication with calculate_string w/o signs."""
    result = calculate_string(f"{num_l}*{num_r}")

    assert result == num_l * num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_multiplication_minus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test multiplication with calculate_string.

    Sign left number: minus
    Sign right number: plus
    """
    result = calculate_string(f"-{num_l}*+{num_r}")

    assert result == -num_l * +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_multiplication_plus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test multiplication with calculate_string.

    Sign left number: plus
    Sign right number: minus
    """
    result = calculate_string(f"+{num_l}*-{num_r}")

    assert result == +num_l * -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_multiplication_minus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test multiplication with calculate_string.

    Sign left number: minus
    Sign right number: minus
    """
    result = calculate_string(f"-{num_l}*-{num_r}")

    assert result == -num_l * -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_multiplication_plus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test multiplication with calculate_string.

    Sign left number: plus
    Sign right number: plus
    """
    result = calculate_string(f"+{num_l}*+{num_r}")

    assert result == +num_l * +num_r


# Division


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
        (_rand_complex_wo_0(), _rand_complex_wo_0()),
    ],
)
def test_division(num_l: NumberType, num_r: NumberType) -> None:
    """Test division with calculate_string w/o signs."""
    result = calculate_string(f"{num_l}/{num_r}")

    assert result == num_l / num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
        (_rand_complex_wo_0(), _rand_complex_wo_0()),
    ],
)
def test_division_minus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test division with calculate_string.

    Sign left number: minus
    Sign right number: plus
    """
    result = calculate_string(f"-{num_l}/+{num_r}")

    assert result == -num_l / +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
        (_rand_complex_wo_0(), _rand_complex_wo_0()),
    ],
)
def test_division_plus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test division with calculate_string.

    Sign left number: plus
    Sign right number: minus
    """
    result = calculate_string(f"+{num_l}/-{num_r}")

    assert result == +num_l / -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
        (_rand_complex_wo_0(), _rand_complex_wo_0()),
    ],
)
def test_division_minus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test division with calculate_string.

    Sign left number: minus
    Sign right number: minus
    """
    result = calculate_string(f"-{num_l}/-{num_r}")

    assert result == -num_l / -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
        (_rand_complex_wo_0(), _rand_complex_wo_0()),
    ],
)
def test_division_plus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test division with calculate_string.

    Sign left number: plus
    Sign right number: plus
    """
    result = calculate_string(f"+{num_l}/+{num_r}")

    assert result == +num_l / +num_r


# Exponentiation


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_wo_0(), _rand_complex_w_0()),
    ],
)
def test_exponentiation(num_l: NumberType, num_r: NumberType) -> None:
    """Test exponentiation with calculate_string w/o signs."""
    result = calculate_string(f"{num_l}**{num_r}")

    assert result == num_l**num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_wo_0(), _rand_complex_w_0()),
    ],
)
def test_exponentiation_minus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test exponentiation with calculate_string.

    Sign left number: minus
    Sign right number: plus
    """
    result = calculate_string(f"-{num_l}**+{num_r}")

    assert result == -(num_l**+num_r)


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_wo_0(), _rand_int_wo_0()),
        (_rand_float_wo_0(), _rand_float_wo_0()),
        (_rand_complex_wo_0(), _rand_complex_wo_0()),
    ],
)
def test_exponentiation_plus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test exponentiation with calculate_string.

    Sign left number: plus
    Sign right number: minus
    """
    result = calculate_string(f"+{num_l}**-{num_r}")

    assert result == +(num_l**-num_r)


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_wo_0(), _rand_int_wo_0()),
        (_rand_float_wo_0(), _rand_float_wo_0()),
        (_rand_complex_wo_0(), _rand_complex_wo_0()),
    ],
)
def test_exponentiation_minus_minus(num_l: NumberType, num_r: NumberType) -> None:
    """Test exponentiation with calculate_string.

    Sign left number: minus
    Sign right number: minus
    """
    result = calculate_string(f"-{num_l}**-{num_r}")

    assert result == -(num_l**-num_r)


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_wo_0(), _rand_complex_w_0()),
    ],
)
def test_exponentiation_plus_plus(num_l: NumberType, num_r: NumberType) -> None:
    """Test exponentiation with calculate_string.

    Sign left number: plus
    Sign right number: plus
    """
    result = calculate_string(f"+{num_l}**+{num_r}")

    assert result == +(num_l**+num_r)


# Floor-division


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_floor_division(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test floor-division with calculate_string w/o signs."""
    result = calculate_string(f"{num_l}//{num_r}")

    assert result == num_l // num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_floor_division_minus_plus(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test floor-division with calculate_string.

    Sign left number: minus
    Sign right number: plus
    """
    result = calculate_string(f"-{num_l}//+{num_r}")

    assert result == -num_l // +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_floor_division_plus_minus(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test floor-division with calculate_string.

    Sign left number: plus
    Sign right number: minus
    """
    result = calculate_string(f"+{num_l}//-{num_r}")

    assert result == +num_l // -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_floor_division_minus_minus(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test floor-division with calculate_string.

    Sign left number: minus
    Sign right number: minus
    """
    result = calculate_string(f"-{num_l}//-{num_r}")

    assert result == -num_l // -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_floor_division_plus_plus(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test floor-division with calculate_string.

    Sign left number: plus
    Sign right number: plus
    """
    result = calculate_string(f"+{num_l}//+{num_r}")

    assert result == +num_l // +num_r


# Modulo


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_modulo(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test modulo with calculate_string w/o signs."""
    result = calculate_string(f"{num_l}%{num_r}")

    assert result == num_l % num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_modulo_minus_plus(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test modulo with calculate_string.

    Sign left number: minus
    Sign right number: plus
    """
    result = calculate_string(f"-{num_l}%+{num_r}")

    assert result == -num_l % +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_modulo_plus_minus(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test modulo with calculate_string.

    Sign left number: plus
    Sign right number: minus
    """
    result = calculate_string(f"+{num_l}%-{num_r}")

    assert result == +num_l % -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_modulo_minus_minus(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test modulo with calculate_string.

    Sign left number: minus
    Sign right number: minus
    """
    result = calculate_string(f"-{num_l}%-{num_r}")

    assert result == -num_l % -num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_modulo_plus_plus(num_l: Union[int, float], num_r: Union[int, float]) -> None:
    """Test modulo with calculate_string.

    Sign left number: plus
    Sign right number: plus
    """
    result = calculate_string(f"+{num_l}%+{num_r}")

    assert result == +num_l % +num_r


# Parenthesis


def test_parenthesis_line_calculation() -> None:
    """Test parenthesis with calculate_string for line calculation."""
    num_1 = _rand_int_w_0()
    num_2 = _rand_int_w_0()
    num_3 = _rand_int_w_0()

    result = calculate_string(f"({num_1}+{num_2})*{num_3}")

    assert result == (num_1 + num_2) * num_3


def test_parenthesis_point_calculation() -> None:
    """Test parenthesis with calculate_string for point calculation."""
    num_1 = _rand_int_w_0()
    num_2 = _rand_int_w_0()
    num_3 = _rand_int_w_0()

    result = calculate_string(f"{num_1}+({num_2}*{num_3})")

    assert result == num_1 + (num_2 * num_3)


# Miscellaneous


def test_empty_str() -> None:
    """Test with empty string."""
    result = calculate_string("")

    assert result is None


def test_error_not_numbertype() -> None:
    """Test ValueError is risen when return type is not NumberType."""
    with pytest.raises(StringCalculatorError, match="could not be calculated due to"):
        calculate_string("True")


def test_error_unsupported_operator() -> None:
    """Test KeyError is risen when return type is not NumberType."""
    with pytest.raises(StringCalculatorError, match="has unsupported node"):
        calculate_string("1 @ 1")
