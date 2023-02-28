"""Tests for `tox_env_exe_runner` module."""
# pylint: disable=protected-access
import os
import subprocess  # noqa: S404
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import pytest

from formelsammlung import env_exe_runner


@contextmanager
def change_cwd(target: Path) -> Generator[None, None, None]:
    """Change cwd with a contextmanager."""
    cwd = os.getcwd()
    os.chdir(target)
    yield
    os.chdir(cwd)


def test_runner_without_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test runner without additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)

    result = env_exe_runner.env_exe_runner(["tox"], ["toxenv"], "tool")

    assert result == 32


def test_runner_with_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test runner with additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)

    result = env_exe_runner.env_exe_runner(["tox"], ["toxenv"], "tool", ["argument"])

    assert result == 32


def test_venv_without_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test venv without additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)

    result = env_exe_runner.env_exe_runner(["venv"], [], "tool")

    assert result == 32


def test_venv_with_args(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test venv with additional arguments."""
    monkeypatch.setattr(subprocess, "call", lambda _: 32)
    monkeypatch.setattr(Path, "is_file", lambda _: True)

    result = env_exe_runner.env_exe_runner(["venv"], [], "tool", ["argument"])

    assert result == 32


def test_no_cmd_found(capsys: pytest.CaptureFixture[str]) -> None:
    """Test exit code 127 on missing cmd."""
    result = env_exe_runner.env_exe_runner(
        ["tox", "venv"], ["non_existing_toxenv"], "no_existing_tool"
    )

    assert result == 127
    output = capsys.readouterr().out
    assert "No 'no_existing_tool' executable found." in output
    assert "- 'tox' envs: ['non_existing_toxenv']" in output
    assert "- virtual env: ['venv']" in output


def test__check_venv_success(tmp_path: Path) -> None:
    """Test return value of _check_venv for success."""
    venv_name = ".venv"
    venv = tmp_path / venv_name
    venv.mkdir()
    filename = "testfile"
    exe = venv / env_exe_runner.EXE.format(tool=filename)
    exe.parent.mkdir()
    exe.write_text("This is a file.")
    #: Change cwd to tmp dir
    # fmt: off
    with change_cwd(tmp_path):

        result = env_exe_runner._check_venv(venv_name, filename)
        # fmt: on

        assert result is not None
        assert result.absolute() == Path(exe)


def test__check_venv_fail(tmp_path: Path) -> None:
    """Test return value of _check_venv for failure."""
    venv_name = ".venv"
    venv = tmp_path / venv_name
    venv.mkdir()
    filename = "testfile"
    #: Change cwd to tmp dir
    # fmt: off
    with change_cwd(tmp_path):

        result = env_exe_runner._check_venv(venv_name, filename)
        # fmt: on

        assert result is None


@pytest.mark.parametrize("runner_name", ["tox", "nox"])
def test__check_runner_envs_success(runner_name: str, tmp_path: Path) -> None:
    """Test return value of _check_runner_envs for success."""
    #: Create runner dir
    runner_dir = tmp_path / ("." + runner_name)
    runner_dir.mkdir()
    #: Create env dirs
    env1_dir = runner_dir / "env1"
    env1_dir.mkdir()
    env2_dir = runner_dir / "env2"
    env2_dir.mkdir()
    #: Create testfile in second env
    filename = "testfile"
    exe = env2_dir / env_exe_runner.EXE.format(tool=filename)
    exe.parent.mkdir()
    exe.write_text("This is a file.")
    #: Change cwd to tmp dir
    # fmt: off
    with change_cwd(tmp_path):

        result = env_exe_runner._check_runner_envs(runner_name, ["env1", "env2"], filename)
        # fmt: on

        assert result is not None
        assert result.absolute() == Path(exe)


@pytest.mark.parametrize("runner_name", ["tox", "nox"])
def test__check_runner_envs_fail(runner_name: str, tmp_path: Path) -> None:
    """Test return value of _check_runner_envs for failure."""
    #: Create runner dir
    runner_dir = tmp_path / ("." + runner_name)
    runner_dir.mkdir()
    #: Create env dirs
    env1_dir = runner_dir / "env1"
    env1_dir.mkdir()
    env2_dir = runner_dir / "env2"
    env2_dir.mkdir()
    filename = "testfile"
    #: Change cwd to tmp dir
    # fmt: off
    with change_cwd(tmp_path):

        result = env_exe_runner._check_runner_envs(runner_name, ["env1", "env2"], filename)
        # fmt: on

        assert result is None
