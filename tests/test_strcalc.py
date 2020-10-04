# noqa: D205,D208,D400
"""
    tests.test_strcalc
    ~~~~~~~~~~~~~~~~~~

    Tests for strcalc.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
import random

import pytest

from formelsammlung.strcalc import calculate_string


@pytest.mark.parametrize(
    ("num_l", "num_r"),
    [
        (random.randrange(100), random.randrange(100)),
        (random.uniform(0, 100), random.uniform(0, 100)),
        (
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(0, 100)}j"
            ),
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(0, 100)}j"
            ),
        ),
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
        (random.randrange(100), random.randrange(100)),
        (random.uniform(0, 100), random.uniform(0, 100)),
        (
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(0, 100)}j"
            ),
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(0, 100)}j"
            ),
        ),
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
        (random.randrange(100), random.randrange(100)),
        (random.uniform(0, 100), random.uniform(0, 100)),
        (
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(0, 100)}j"
            ),
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(0, 100)}j"
            ),
        ),
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
        (random.randrange(100), random.randrange(1, 100)),
        (random.uniform(0, 100), random.uniform(1, 100)),
        (
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(1, 100)}j"
            ),
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(1, 100)}j"
            ),
        ),
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
        (random.randrange(100), random.randrange(100)),
        (random.uniform(0, 100), random.uniform(0, 100)),
        (
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(0, 100)}j"
            ),
            complex(
                f"{random.uniform(0, 100)}"
                f"{random.choice(('+', '-'))}{random.uniform(0, 100)}j"
            ),
        ),
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
        (random.randrange(100), random.randrange(1, 100)),
        (random.uniform(0, 100), random.uniform(1, 100)),
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
        (random.randrange(100), random.randrange(1, 100)),
        (random.uniform(0, 100), random.uniform(1, 100)),
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
    num_1 = random.randrange(100)
    num_2 = random.randrange(100)
    num_3 = random.randrange(100)
    assert calculate_string(f"({num_1}+{num_2})*{num_3}") == (num_1 + num_2) * num_3
    assert calculate_string(f"{num_1}+({num_2}*{num_3})") == num_1 + (num_2 * num_3)


def test_empty_str():
    """Test with empty string."""
    assert calculate_string("") is None
