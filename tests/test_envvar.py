# noqa: D205,D208,D400
"""
    tests.test_envvar
    ~~~~~~~~~~~~~~~~~

    Tests for envvar.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
from decimal import Decimal

import pytest

from formelsammlung.envvar import (
    getenv_typed as get,
    TRUE_BOOL_VALUES,
    FALSE_BOOL_VALUES,
)


def test_default():
    """Test default."""
    assert get("TEST_DEFAULT") is None
    assert get("TEST_DEFAULT", "DefaultValue") == "DefaultValue"


def test_raise_error_no_value():
    """Test raising KeyError."""
    assert get("TEST_NO_VALUE_ERROR", raise_error_if_no_value=False) is None
    with pytest.raises(KeyError):
        get("TEST_NO_VALUE_ERROR", raise_error_if_no_value=True)


def test_type_conversion(monkeypatch):
    """Test type conversion."""
    assert get("TEST_CONVERSION") is None
    monkeypatch.setenv("TEST_CONVERSION", "1.1")
    assert get("TEST_CONVERSION", rv_type=Decimal) == Decimal("1.1")


def test_string_guessing(monkeypatch):
    """Test string type guessing."""
    assert get("TEST_STRING") is None
    monkeypatch.setenv("TEST_STRING", "JustAString")
    assert get("TEST_STRING") == "JustAString"


def test_number_guessing(monkeypatch):
    """Test number type guessing."""
    assert get("TEST_INTEGER") is None
    assert get("TEST_FLOAT") is None
    monkeypatch.setenv("TEST_INTEGER", "123")
    monkeypatch.setenv("TEST_FLOAT", "1.23")
    assert get("TEST_INTEGER") == 123
    assert get("TEST_FLOAT") == 1.23


@pytest.mark.parametrize(
    ("bool_alias", "bool_val_default", "bool_val_altered"),
    [(tbv, True, int(tbv) if tbv.isdigit() else tbv) for tbv in TRUE_BOOL_VALUES]
    + [("fake_true", "fake_true", True)],
)
def test_true_bool_guessing(
    bool_alias, bool_val_default, bool_val_altered, monkeypatch
):
    """Test true bool type guessing."""
    assert get("TEST_BOOL") is None
    with monkeypatch.context() as mp:
        mp.setenv("TEST_BOOL", str(bool_alias))
        assert get("TEST_BOOL") == bool_val_default

    assert get("TEST_BOOL") is None
    with monkeypatch.context() as mp:
        mp.setenv("TEST_BOOL", str(bool_alias))
        assert get("TEST_BOOL", true_bool_values=["fake_true"]) == bool_val_altered


@pytest.mark.parametrize(
    ("bool_alias", "bool_val_default", "bool_val_altered"),
    [(fbv, False, int(fbv) if fbv.isdigit() else fbv) for fbv in FALSE_BOOL_VALUES]
    + [("fake_false", "fake_false", False)],
)
def test_false_bool_guessing(
    bool_alias, bool_val_default, bool_val_altered, monkeypatch
):
    """Test false bool type guessing."""
    assert get("TEST_BOOL") is None
    with monkeypatch.context() as mp:
        mp.setenv("TEST_BOOL", str(bool_alias))
        assert get("TEST_BOOL") == bool_val_default

    assert get("TEST_BOOL") is None
    with monkeypatch.context() as mp:
        mp.setenv("TEST_BOOL", str(bool_alias))
        assert get("TEST_BOOL", false_bool_values=["fake_false"]) == bool_val_altered


def test_raise_wrong_bool_value(monkeypatch):
    assert get("TEST_BOOL_ERROR") is None
    monkeypatch.setenv("TEST_BOOL_ERROR", "True")
    assert get("TEST_BOOL_ERROR", rv_type=bool) is True
    monkeypatch.setenv("TEST_BOOL_ERROR", "no_bool")
    with pytest.raises(KeyError):
        get("TEST_BOOL_ERROR", rv_type=bool)
