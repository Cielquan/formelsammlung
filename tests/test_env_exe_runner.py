# noqa: D205,D208,D400
"""
    tests.test_tox_env_exe_runner
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for tox_env_exe_runner.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
import subprocess

from pathlib import Path

from formelsammlung.env_exe_runner import env_exe_runner as runner


def test_without_args(monkeypatch):
    """Test runner without additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)
    assert runner("tox", ["toxenv"], "tool") == 32


def test_with_args(monkeypatch):
    """Test runner with additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)
    assert runner("tox", ["toxenv"], "tool", ["argument"]) == 32


def test_no_cmd_found(capsys):
    """Test exit code 127 on missing cmd."""
    assert runner("tox", ["non_existing_toxenv"], "no_existing_tool") == 127
    assert "No 'no_existing_tool' executable found." in capsys.readouterr().out


def test_invalid_runner(capsys):
    """Test exit code 127 on invalid runner."""
    assert runner("not_tox_nor_nox", ["non_existing_toxenv"], "no_existing_tool") == 127
    assert "No valid runner was given." in capsys.readouterr().out
