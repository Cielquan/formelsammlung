"""Tests for `envvar` module."""

# pylint: disable=protected-access
import re
from decimal import Decimal
from typing import Union

import pytest

from formelsammlung.envvar import (
    FALSE_BOOL_VALUES,
    FLOAT_REGEX,
    INT_REGEX,
    TRUE_BOOL_VALUES,
    EnvVarGetter,
    getenv_typed as get,
)


def test_default() -> None:
    """Test default."""
    assert get("TEST_DEFAULT") is None

    result = get("TEST_DEFAULT", "DefaultValue")

    assert result == "DefaultValue"


def test_raise_error_no_value() -> None:
    """Test raising KeyError."""
    assert get("TEST_NO_VALUE_ERROR", raise_error_if_no_value=False) is None

    with pytest.raises(KeyError):
        get("TEST_NO_VALUE_ERROR", raise_error_if_no_value=True)


def test_type_conversion(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test type conversion."""
    assert get("TEST_CONVERSION") is None
    monkeypatch.setenv("TEST_CONVERSION", "1.1")

    result = get("TEST_CONVERSION", rv_type=Decimal)

    assert result == Decimal("1.1")


def test_string_guessing(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test string type guessing."""
    assert get("TEST_STRING") is None
    monkeypatch.setenv("TEST_STRING", "JustAString")

    result = get("TEST_STRING")

    assert result == "JustAString"


def test_number_guessing_int(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test number type guessing."""
    assert get("TEST_INTEGER") is None
    monkeypatch.setenv("TEST_INTEGER", "123")

    result = get("TEST_INTEGER")

    assert result == 123


def test_number_guessing_float(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test number type guessing."""
    assert get("TEST_FLOAT") is None
    monkeypatch.setenv("TEST_FLOAT", "1.23")

    result = get("TEST_FLOAT")

    assert result == 1.23


@pytest.mark.parametrize(
    ("bool_alias", "bool_val_default"),
    [(tbv, True) for tbv in TRUE_BOOL_VALUES] + [("fake_true", "fake_true")],
)
def test_true_bool_guessing(
    bool_alias: str,
    bool_val_default: Union[bool, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test True bool type guessing."""
    assert get("TEST_BOOL") is None
    monkeypatch.setenv("TEST_BOOL", str(bool_alias))

    result = get("TEST_BOOL")

    assert result == bool_val_default


@pytest.mark.parametrize(
    ("bool_alias", "bool_val_altered"),
    [(tbv, int(tbv) if tbv.isdigit() else tbv) for tbv in TRUE_BOOL_VALUES] + [("fake_true", True)],
)
def test_true_bool_guessing_w_true_bool_values(
    bool_alias: str,
    bool_val_altered: Union[bool, str, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test True bool type guessing w/ true_bool_values set."""
    assert get("TEST_BOOL") is None
    monkeypatch.setenv("TEST_BOOL", str(bool_alias))

    result = get("TEST_BOOL", true_bool_values=["fake_true"])

    assert result == bool_val_altered


@pytest.mark.parametrize(
    ("bool_alias", "bool_val_default"),
    [(fbv, False) for fbv in FALSE_BOOL_VALUES] + [("fake_false", "fake_false")],
)
def test_false_bool_guessing(
    bool_alias: str,
    bool_val_default: Union[bool, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test False bool type guessing."""
    assert get("TEST_BOOL") is None
    monkeypatch.setenv("TEST_BOOL", str(bool_alias))

    result = get("TEST_BOOL")

    assert result == bool_val_default


@pytest.mark.parametrize(
    ("bool_alias", "bool_val_altered"),
    [(fbv, int(fbv) if fbv.isdigit() else fbv) for fbv in FALSE_BOOL_VALUES]
    + [("fake_false", False)],
)
def test_false_bool_guessing_w_false_bool_values(
    bool_alias: str,
    bool_val_altered: Union[bool, str, int],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test False bool type guessing w/ false_bool_values set."""
    assert get("TEST_BOOL") is None
    monkeypatch.setenv("TEST_BOOL", str(bool_alias))

    result = get("TEST_BOOL", false_bool_values=["fake_false"])

    assert result == bool_val_altered


def test_raise_wrong_bool_value(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test raising KeyError on wrong bool value."""
    assert get("TEST_BOOL_ERROR") is None
    #: assert function works
    monkeypatch.setenv("TEST_BOOL_ERROR", "True")
    assert get("TEST_BOOL_ERROR", rv_type=bool) is True
    #: set error value
    monkeypatch.setenv("TEST_BOOL_ERROR", "no_bool")

    with pytest.raises(KeyError):
        get("TEST_BOOL_ERROR", rv_type=bool)


# Test class


def test_EnvVarGetter_init() -> None:  # noqa: C0103,N802
    """Test constructor of EnvVarGetter."""
    instance = EnvVarGetter()

    result = instance.int_regex_pattern

    assert result == re.compile(INT_REGEX)


def test_EnvVarGetter_true_bool_values_getter() -> None:  # noqa: C0103,N802
    """Test true_bool_values getter of EnvVarGetter."""
    instance = EnvVarGetter()

    result = instance.true_bool_values

    assert result == set(TRUE_BOOL_VALUES)


def test_EnvVarGetter_true_bool_values_setter() -> None:  # noqa: C0103,N802
    """Test true_bool_values setter of EnvVarGetter."""
    instance = EnvVarGetter()
    new_value = {"fake_true"}
    instance.true_bool_values = new_value

    result = instance.true_bool_values

    assert result == new_value


def test_EnvVarGetter_false_bool_values_getter() -> None:  # noqa: C0103,N802
    """Test false_bool_values getter of EnvVarGetter."""
    instance = EnvVarGetter()

    result = instance.false_bool_values

    assert result == set(FALSE_BOOL_VALUES)


def test_EnvVarGetter_false_bool_values_setter() -> None:  # noqa: C0103,N802
    """Test false_bool_values setter of EnvVarGetter."""
    instance = EnvVarGetter()
    new_value = {"fake_false"}
    instance.false_bool_values = new_value

    result = instance.false_bool_values

    assert result == new_value


def test_EnvVarGetter_int_regex_getter() -> None:  # noqa: C0103,N802
    """Test int_regex getter of EnvVarGetter."""
    instance = EnvVarGetter()

    result = instance.int_regex

    assert result == INT_REGEX


def test_EnvVarGetter_int_regex_setter() -> None:  # noqa: C0103,N802
    """Test int_regex setter of EnvVarGetter."""
    instance = EnvVarGetter()
    new_value = "int-regex"
    instance.int_regex = new_value

    result = instance

    assert result.int_regex == new_value
    assert result.int_regex_pattern == re.compile(new_value)


def test_EnvVarGetter_int_regex_pattern_getter() -> None:  # noqa: C0103,N802
    """Test int_regex_pattern getter of EnvVarGetter."""
    instance = EnvVarGetter()

    result = instance.int_regex_pattern

    assert result == re.compile(INT_REGEX)


def test_EnvVarGetter_int_regex_pattern_setter() -> None:  # noqa: C0103,N802
    """Test int_regex_pattern setter of EnvVarGetter."""
    instance = EnvVarGetter()

    with pytest.raises(AttributeError, match="int_regex_pattern"):
        instance.int_regex_pattern = re.compile("")


def test_EnvVarGetter_float_regex_getter() -> None:  # noqa: C0103,N802
    """Test float_regex getter of EnvVarGetter."""
    instance = EnvVarGetter()

    result = instance.float_regex

    assert result == FLOAT_REGEX


def test_EnvVarGetter_float_regex_setter() -> None:  # noqa: C0103,N802
    """Test float_regex setter of EnvVarGetter."""
    instance = EnvVarGetter()
    new_value = "int-regex"
    instance.float_regex = new_value

    result = instance

    assert result.float_regex == new_value
    assert result.float_regex_pattern == re.compile(new_value)


def test_EnvVarGetter_float_regex_pattern_getter() -> None:  # noqa: C0103,N802
    """Test float_regex_pattern getter of EnvVarGetter."""
    instance = EnvVarGetter()

    result = instance.float_regex_pattern

    assert result == re.compile(FLOAT_REGEX)


def test_EnvVarGetter_float_regex_pattern_setter() -> None:  # noqa: C0103,N802
    """Test float_regex_pattern setter of EnvVarGetter."""
    instance = EnvVarGetter()

    with pytest.raises(AttributeError, match="float_regex_pattern"):
        instance.float_regex_pattern = re.compile("")


def test_EnvVarGetter__guess_bool_true() -> None:  # noqa: C0103,N802
    """Test _guess_bool of EnvVarGetter for True."""
    instance = EnvVarGetter()

    result = instance._guess_bool("yes")

    assert result is True


def test_EnvVarGetter__guess_bool_false() -> None:  # noqa: C0103,N802
    """Test _guess_bool of EnvVarGetter for False."""
    instance = EnvVarGetter()

    result = instance._guess_bool("no")

    assert result is False


def test_EnvVarGetter__guess_bool_none() -> None:  # noqa: C0103,N802
    """Test _guess_bool of EnvVarGetter for None."""
    instance = EnvVarGetter()

    result = instance._guess_bool("no-bool")

    assert result is None


def test_EnvVarGetter__guess_num_int() -> None:  # noqa: C0103,N802
    """Test _guess_num of EnvVarGetter for int."""
    instance = EnvVarGetter()

    result = instance._guess_num("32")

    assert result == 32


def test_EnvVarGetter__guess_num_float() -> None:  # noqa: C0103,N802
    """Test _guess_num of EnvVarGetter for float."""
    instance = EnvVarGetter()

    result = instance._guess_num("32.69")

    assert result == 32.69


def test_EnvVarGetter__guess_num_none() -> None:  # noqa: C0103,N802
    """Test _guess_num of EnvVarGetter for none."""
    instance = EnvVarGetter()

    result = instance._guess_num("no-number")

    assert result is None
