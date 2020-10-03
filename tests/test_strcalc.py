# noqa: D205,D208,D400
"""
    tests.test_strcalc
    ~~~~~~~~~~~~~~~~~~

    Tests for strcalc.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
import random

from typing import List, Tuple

from formelsammlung.strcalc import calculate_string, T_Number


def _number_generator(
    left_num_min: int = 0,
    left_num_max: int = 100,
    right_num_min: int = 0,
    right_num_max: int = 100,
    include_complex: bool = True,
) -> List[Tuple[T_Number, T_Number]]:
    """Generate list with random number pairs for tests.

    :param left_num_min: Minimum for range of left number, defaults to 0
    :param left_num_max: Maximum for range of left number, defaults to 100
    :param right_num_min: Minimum for range of right number, defaults to 0
    :param right_num_max: Maximum for range of right number, defaults to 100
    :param include_complex: Bool if a pair of complex numbers should be included
        defaults to True
    :return: List of tuples with number pairs
    """
    number_list: List[Tuple[T_Number, T_Number]] = [
        (random.randrange(left_num_max), random.randrange(right_num_max)),
        (
            random.uniform(left_num_min, left_num_max),
            random.uniform(right_num_min, right_num_max),
        ),
    ]

    if include_complex:
        number_list.append(
            (
                complex(
                    f"{random.uniform(left_num_min, left_num_max)}"
                    f"{random.choice(('+', '-'))}"
                    f"{random.uniform(left_num_min, left_num_max)}j"
                ),
                complex(
                    f"{random.uniform(right_num_min, right_num_max)}"
                    f"{random.choice(('+', '-'))}"
                    f"{random.uniform(right_num_min, right_num_max)}j"
                ),
            )
        )

    return number_list


def test_addition():
    """Test addition with """
    for num_pair in _number_generator():
        num_l, num_r = num_pair[0], num_pair[1]
        assert calculate_string(f"{num_l}+{num_r}") == num_l + num_r
        assert calculate_string(f"-{num_l}++{num_r}") == -num_l + +num_r
        assert calculate_string(f"+{num_l}+-{num_r}") == +num_l + -num_r
        assert calculate_string(f"-{num_l}+-{num_r}") == -num_l + -num_r
        assert calculate_string(f"+{num_l}++{num_r}") == +num_l + +num_r


def test_subtraction():
    """Test subtraction with """
    for num_pair in _number_generator():
        num_l, num_r = num_pair[0], num_pair[1]
        assert calculate_string(f"{num_l}-{num_r}") == num_l - num_r
        assert calculate_string(f"-{num_l}-+{num_r}") == -num_l - +num_r
        assert calculate_string(f"+{num_l}--{num_r}") == +num_l - -num_r
        assert calculate_string(f"-{num_l}--{num_r}") == -num_l - -num_r
        assert calculate_string(f"+{num_l}-+{num_r}") == +num_l - +num_r


def test_multiplication():
    """Test multiplication with """
    for num_pair in _number_generator():
        num_l, num_r = num_pair[0], num_pair[1]
        assert calculate_string(f"{num_l}*{num_r}") == num_l * num_r
        assert calculate_string(f"-{num_l}*+{num_r}") == -num_l * +num_r
        assert calculate_string(f"+{num_l}*-{num_r}") == +num_l * -num_r
        assert calculate_string(f"-{num_l}*-{num_r}") == -num_l * -num_r
        assert calculate_string(f"+{num_l}*+{num_r}") == +num_l * +num_r


def test_true_division():
    """Test division with """
    for num_pair in _number_generator(right_num_min=1):
        num_l, num_r = num_pair[0], num_pair[1]
        assert calculate_string(f"{num_l}/{num_r}") == num_l / num_r
        assert calculate_string(f"-{num_l}/+{num_r}") == -num_l / +num_r
        assert calculate_string(f"+{num_l}/-{num_r}") == +num_l / -num_r
        assert calculate_string(f"-{num_l}/-{num_r}") == -num_l / -num_r
        assert calculate_string(f"+{num_l}/+{num_r}") == +num_l / +num_r


def test_exponentiation():
    """Test exponentiation with """
    for num_pair in _number_generator():
        num_l, num_r = num_pair[0], num_pair[1]
        assert calculate_string(f"{num_l}**{num_r}") == num_l ** num_r
        assert calculate_string(f"-{num_l}**+{num_r}") == -(num_l ** +num_r)
        assert calculate_string(f"+{num_l}**-{num_r}") == +(num_l ** -num_r)
        assert calculate_string(f"-{num_l}**-{num_r}") == -(num_l ** -num_r)
        assert calculate_string(f"+{num_l}**+{num_r}") == +(num_l ** +num_r)


def test_floor_division():
    """Test floor-division with """
    for num_pair in _number_generator(right_num_min=1, include_complex=False):
        num_l, num_r = num_pair[0], num_pair[1]
        assert calculate_string(f"{num_l}//{num_r}") == num_l // num_r
        assert calculate_string(f"-{num_l}//+{num_r}") == -num_l // +num_r
        assert calculate_string(f"+{num_l}//-{num_r}") == +num_l // -num_r
        assert calculate_string(f"-{num_l}//-{num_r}") == -num_l // -num_r
        assert calculate_string(f"+{num_l}//+{num_r}") == +num_l // +num_r


def test_modulo():
    """Test modulo with """
    for num_pair in _number_generator(right_num_min=1, include_complex=False):
        num_l, num_r = num_pair[0], num_pair[1]
        assert calculate_string(f"{num_l}%{num_r}") == num_l % num_r
        assert calculate_string(f"-{num_l}%+{num_r}") == -num_l % +num_r
        assert calculate_string(f"+{num_l}%-{num_r}") == +num_l % -num_r
        assert calculate_string(f"-{num_l}%-{num_r}") == -num_l % -num_r
        assert calculate_string(f"+{num_l}%+{num_r}") == +num_l % +num_r


def test_parenthesis():
    """Test parenthesis with """
    num_1 = random.randrange(100)
    num_2 = random.randrange(100)
    num_3 = random.randrange(100)
    assert calculate_string(f"({num_1}+{num_2})*{num_3}") == (num_1 + num_2) * num_3
    assert calculate_string(f"{num_1}+({num_2}*{num_3})") == num_1 + (num_2 * num_3)


def test_empty_str():
    """Test with empty string."""
    assert calculate_string("") is None
