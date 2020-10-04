# noqa: D205,D208,D400
"""
    tests.test_strcalc
    ~~~~~~~~~~~~~~~~~~

    Tests for strcalc.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
import random
import sys

import pytest

from formelsammlung.strcalc import calculate_string


def _rand_int_w_0():
    """Return random positive integer."""
    return random.randrange(100)


def _rand_int_wo_0():
    """Return random positive integer without zero."""
    return random.randrange(1, 100)


def _rand_float_w_0():
    """Return random positive float."""
    return random.uniform(0, 100)


def _rand_float_wo_0():
    """Return random positive float without zero."""
    return random.uniform(1, 100)


def _rand_complex_w_0():
    """Return random positive complex number.

    The number is made of floats for real and imag part.
    The imag part is randomly positive or negative.
    """
    if hasattr(sys, "pypy_version_info"):
        return complex(
            f"{_rand_float_w_0():.10f}"
            f"{random.choice(('+', '-'))}{_rand_float_w_0():.10f}j"
        )
    return complex(
        f"{_rand_float_w_0()}{random.choice(('+', '-'))}{_rand_float_w_0()}j"
    )


def _rand_complex_wo_0():
    """Return random positive complex number without zero.

    The number is made of floats for real and imag part.
    The imag part is randomly positive or negative.
    """
    if hasattr(sys, "pypy_version_info"):
        return complex(
            f"{_rand_float_wo_0():.10f}"
            f"{random.choice(('+', '-'))}{_rand_float_wo_0():.10f}j"
        )
    return complex(
        f"{_rand_float_wo_0()}{random.choice(('+', '-'))}{_rand_float_wo_0()}j"
    )


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (_rand_int_w_0(), _rand_int_w_0()),
        (_rand_float_w_0(), _rand_float_w_0()),
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_addition(num_l, num_r):
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
def test_subtraction(num_l, num_r):
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
def test_multiplication(num_l, num_r):
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
def test_true_division(num_l, num_r):
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
        (_rand_complex_w_0(), _rand_complex_w_0()),
    ],
)
def test_exponentiation(num_l, num_r):
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
def test_floor_division(num_l, num_r):
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
def test_modulo(num_l, num_r):
    """Test modulo with calculate_string."""
    assert calculate_string(f"{num_l}%{num_r}") == num_l % num_r
    assert calculate_string(f"-{num_l}%+{num_r}") == -num_l % +num_r
    assert calculate_string(f"+{num_l}%-{num_r}") == +num_l % -num_r
    assert calculate_string(f"-{num_l}%-{num_r}") == -num_l % -num_r
    assert calculate_string(f"+{num_l}%+{num_r}") == +num_l % +num_r


def test_parenthesis():
    """Test parenthesis with calculate_string."""
    num_1 = _rand_int_w_0()
    num_2 = _rand_int_w_0()
    num_3 = _rand_int_w_0()
    assert calculate_string(f"({num_1}+{num_2})*{num_3}") == (num_1 + num_2) * num_3
    assert calculate_string(f"{num_1}+({num_2}*{num_3})") == num_1 + (num_2 * num_3)


def test_empty_str():
    """Test with empty string."""
    assert calculate_string("") is None
