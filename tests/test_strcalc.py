"""
    tests.test_strcalc
    ~~~~~~~~~~~~~~~~~~

    Tests for strcalc.py.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
import random

import pytest

from formelsammlung.strcalc import NumberType, calculate_string


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

    The number is made of int for real and imag part.
    The imag part is randomly positive or negative.
    """
    return complex(
        f"{_rand_int_w_0()}{random.choice(('+', '-'))}{_rand_int_w_0()}j"  # noqa: S311
    )


def _rand_complex_wo_0() -> complex:
    """Return random positive complex number without zero.

    The number is made of ints for real and imag part.
    The imag part is randomly positive or negative.
    """
    return complex(
        f"{_rand_int_wo_0()}"  # noqa; S311
        f"{random.choice(('+', '-'))}{_rand_int_wo_0()}j"  # noqa: S311
    )


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_addition(num_l: NumberType, num_r: NumberType) -> None:
    """Test addition with calculate_string."""
    assert calculate_string(f"{num_l}+{num_r}") == num_l + num_r
    assert calculate_string(f"-{num_l}++{num_r}") == -num_l + +num_r
    assert calculate_string(f"+{num_l}+-{num_r}") == +num_l + -num_r
    assert calculate_string(f"-{num_l}+-{num_r}") == -num_l + -num_r
    assert calculate_string(f"+{num_l}++{num_r}") == +num_l + +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_subtraction(num_l: NumberType, num_r: NumberType) -> None:
    """Test subtraction with calculate_string."""
    assert calculate_string(f"{num_l}-{num_r}") == num_l - num_r
    assert calculate_string(f"-{num_l}-+{num_r}") == -num_l - +num_r
    assert calculate_string(f"+{num_l}--{num_r}") == +num_l - -num_r
    assert calculate_string(f"-{num_l}--{num_r}") == -num_l - -num_r
    assert calculate_string(f"+{num_l}-+{num_r}") == +num_l - +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_multiplication(num_l: NumberType, num_r: NumberType) -> None:
    """Test multiplication with calculate_string."""
    assert calculate_string(f"{num_l}*{num_r}") == num_l * num_r
    assert calculate_string(f"-{num_l}*+{num_r}") == -num_l * +num_r
    assert calculate_string(f"+{num_l}*-{num_r}") == +num_l * -num_r
    assert calculate_string(f"-{num_l}*-{num_r}") == -num_l * -num_r
    assert calculate_string(f"+{num_l}*+{num_r}") == +num_l * +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
        (_rand_complex_wo_0(), _rand_complex_wo_0()),
    ],
)
def test_true_division(num_l: NumberType, num_r: NumberType) -> None:
    """Test division with calculate_string."""
    assert calculate_string(f"{num_l}/{num_r}") == num_l / num_r
    assert calculate_string(f"-{num_l}/+{num_r}") == -num_l / +num_r
    assert calculate_string(f"+{num_l}/-{num_r}") == +num_l / -num_r
    assert calculate_string(f"-{num_l}/-{num_r}") == -num_l / -num_r
    assert calculate_string(f"+{num_l}/+{num_r}") == +num_l / +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_wo_0(), _rand_complex_w_0()),
    ],
)
def test_exponentiation(num_l: NumberType, num_r: NumberType) -> None:
    """Test exponentiation with calculate_string."""
    assert calculate_string(f"{num_l}**{num_r}") == num_l ** num_r
    assert calculate_string(f"-{num_l}**+{num_r}") == -(num_l ** +num_r)
    assert calculate_string(f"+{num_l}**+{num_r}") == +(num_l ** +num_r)
    num_l += 1
    num_r += 1
    assert calculate_string(f"+{num_l}**-{num_r}") == +(num_l ** -num_r)
    assert calculate_string(f"-{num_l}**-{num_r}") == -(num_l ** -num_r)


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_floor_division(num_l: NumberType, num_r: NumberType) -> None:
    """Test floor-division with calculate_string."""
    assert calculate_string(f"{num_l}//{num_r}") == num_l // num_r
    assert calculate_string(f"-{num_l}//+{num_r}") == -num_l // +num_r
    assert calculate_string(f"+{num_l}//-{num_r}") == +num_l // -num_r
    assert calculate_string(f"-{num_l}//-{num_r}") == -num_l // -num_r
    assert calculate_string(f"+{num_l}//+{num_r}") == +num_l // +num_r


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_wo_0()),
        (_rand_float_w_0(), _rand_float_wo_0()),
    ],
)
def test_modulo(num_l: NumberType, num_r: NumberType) -> None:
    """Test modulo with calculate_string."""
    assert calculate_string(f"{num_l}%{num_r}") == num_l % num_r
    assert calculate_string(f"-{num_l}%+{num_r}") == -num_l % +num_r
    assert calculate_string(f"+{num_l}%-{num_r}") == +num_l % -num_r
    assert calculate_string(f"-{num_l}%-{num_r}") == -num_l % -num_r
    assert calculate_string(f"+{num_l}%+{num_r}") == +num_l % +num_r


def test_parenthesis() -> None:
    """Test parenthesis with calculate_string."""
    num_1 = _rand_int_w_0()
    num_2 = _rand_int_w_0()
    num_3 = _rand_int_w_0()
    assert calculate_string(f"({num_1}+{num_2})*{num_3}") == (num_1 + num_2) * num_3
    assert calculate_string(f"{num_1}+({num_2}*{num_3})") == num_1 + (num_2 * num_3)


def test_empty_str() -> None:
    """Test with empty string."""
    assert calculate_string("") is None
