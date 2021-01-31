"""
    tests.test_tox_env_exe_runner
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for tox_env_exe_runner.py.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
import subprocess  # noqa: S404

from pathlib import Path

import pytest

from formelsammlung.env_exe_runner import env_exe_runner as runner


def test_runner_without_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test runner without additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)

    result = runner(["tox"], ["toxenv"], "tool")

    assert result == 32


def test_runner_with_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test runner with additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)

    result = runner(["tox"], ["toxenv"], "tool", ["argument"])

    assert result == 32


def test_venv_without_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test venv without additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)

    result = runner(["venv"], [], "tool")

    assert result == 32


def test_venv_with_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test venv with additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)

    result = runner(["venv"], [], "tool", ["argument"])

    assert result == 32


def test_no_cmd_found(capsys: pytest.CaptureFixture) -> None:
    """Test exit code 127 on missing cmd."""
    result = runner(["tox", "venv"], ["non_existing_toxenv"], "no_existing_tool")

    assert result == 127
    output = capsys.readouterr().out
    assert "No 'no_existing_tool' executable found." in output
    assert "- 'tox' envs: ['non_existing_toxenv']" in output
    assert "- virtual env: ['venv']" in output
