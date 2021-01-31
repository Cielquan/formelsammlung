"""
    tests.test_envvar
    ~~~~~~~~~~~~~~~~~

    Tests for envvar.py.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
from decimal import Decimal
from typing import Union

import pytest

from formelsammlung.envvar import FALSE_BOOL_VALUES, TRUE_BOOL_VALUES
from formelsammlung.envvar import getenv_typed as get


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
    [(tbv, True) for tbv in TRUE_BOOL_VALUES]
    + [("fake_true", "fake_true")],  # type: ignore[list-item]
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
    [(tbv, int(tbv) if tbv.isdigit() else tbv) for tbv in TRUE_BOOL_VALUES]
    + [("fake_true", True)],
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
    [(fbv, False) for fbv in FALSE_BOOL_VALUES]
    + [("fake_false", "fake_false")],  # type: ignore[list-item]
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
