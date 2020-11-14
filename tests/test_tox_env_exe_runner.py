# noqa: D205,D208,D400
"""
    tests.test_tox_env_exe_runner
    ~~~~~~~~~~~~~~~~~~

    Tests for test_tox_env_exe_runner.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""
import random
import sys
import subprocess
from pathlib import Path

import pytest

from formelsammlung.tox_env_exe_runner import tox_env_exe_runner as runner


def test_without_args(monkeypatch):
    """Test runner without additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)
    assert runner("tool", ["toxenv"]) == 32


def test_with_args(monkeypatch):
    """Test runner with additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)
    assert runner("tool", ["toxenv"], ["argument"]) == 32


def test_no_cmd_found(capsys):
    """Test exit code 127 on missing cmd."""
    assert runner("no_existing_tool", ["non_existing_toxenv"]) == 127
    assert "No 'no_existing_tool' executable found." in capsys.readouterr().out
