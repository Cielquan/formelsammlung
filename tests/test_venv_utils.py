"""Tests for `venv_utils` module."""
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

import pytest

from formelsammlung import venv_utils


#: Test get_venv_path()
def test_get_venv_path_w_real_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test get_venv_path return when sys.real_prefix is set."""
    sys.real_prefix = ""  # type: ignore[attr-defined]
    monkeypatch.setattr(sys, "real_prefix", "path-to-venv-via-real_prefix")

    result = venv_utils.get_venv_path()

    assert result == Path("path-to-venv-via-real_prefix")


def test_get_venv_path_w_prefix(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test get_venv_path return when sys.real_prefix is not set."""
    monkeypatch.delattr(sys, "real_prefix", raising=False)
    monkeypatch.setattr(sys, "prefix", "path-to-venv-via-prefix")

    result = venv_utils.get_venv_path()

    assert result == Path("path-to-venv-via-prefix")


def test_get_venv_path_raise(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test get_venv_path raising exception on no found venv."""
    monkeypatch.delattr(sys, "real_prefix", raising=False)
    monkeypatch.setattr(sys, "prefix", sys.base_prefix)

    with pytest.raises(FileNotFoundError) as excinfo:
        venv_utils.get_venv_path()

    assert "No calling venv could" in str(excinfo.value)


#: Test get_venv_bin_dir()
def test_get_venv_bin_dir(tmp_path: Path) -> None:
    """Test get_venv_bin_dir return a venv's bin/Scripts dir."""
    fake_venv = tmp_path / ".venv"
    bin_dir = fake_venv / venv_utils.OS_BIN
    bin_dir.mkdir(parents=True)

    result = venv_utils.get_venv_bin_dir(fake_venv)

    assert result == bin_dir


def test_get_venv_bin_dir_raise(tmp_path: Path) -> None:
    """Test get_venv_bin_dir raising exception on no found dir."""
    fake_venv = tmp_path / ".venv"
    fake_venv.mkdir(parents=True)

    with pytest.raises(FileNotFoundError) as excinfo:
        venv_utils.get_venv_bin_dir(fake_venv)

    assert "Given venv has no" in str(excinfo.value)


#: Test get_venv_tmp_dir()
@pytest.mark.parametrize("tmp_dir_name", ["tmp", "temp", ".tmp", ".temp"])
def test_get_venv_tmp_dir(tmp_dir_name: str, tmp_path: Path) -> None:
    """Test get_venv_tmp_dir return a venv's tmp dir."""
    fake_venv = tmp_path / ".venv"
    tmp_dir = fake_venv / tmp_dir_name
    tmp_dir.mkdir(parents=True)

    result = venv_utils.get_venv_tmp_dir(fake_venv)

    assert result == tmp_dir


def test_get_venv_tmp_dir_custom_search(tmp_path: Path) -> None:
    """Test get_venv_tmp_dir finding custom temp dirs."""
    fake_venv = tmp_path / ".venv"
    tmp_dir = fake_venv / "custom_tmp"
    tmp_dir.mkdir(parents=True)

    result = venv_utils.get_venv_tmp_dir(fake_venv, search_tmp_dirs=("custom_tmp",))

    assert result == tmp_dir


@pytest.mark.parametrize(
    ("tmp_dir_name", "create_dir_name"), [("custom_temp", "custom_temp"), ("tmp", None)]
)
def test_get_venv_tmp_dir_create_if_missing(
    tmp_dir_name: str, create_dir_name: Optional[str], tmp_path: Path
) -> None:
    """Test get_venv_tmp_dir creating tmp dirs if missing."""
    fake_venv = tmp_path / ".venv"
    fake_venv.mkdir(parents=True)
    tmp_dir = fake_venv / tmp_dir_name

    result = venv_utils.get_venv_tmp_dir(
        fake_venv, create_if_missing=True, create_dir_name=create_dir_name
    )

    assert result == tmp_dir


def test_get_venv_tmp_dir_raise(tmp_path: Path) -> None:
    """Test get_venv_tmp_dir raising exception on no found dir."""
    fake_venv = tmp_path / ".venv"
    fake_venv.mkdir(parents=True)

    with pytest.raises(FileNotFoundError) as excinfo:
        venv_utils.get_venv_tmp_dir(fake_venv)

    assert "Given venv has no" in str(excinfo.value)


#: Test get_venv_site_packages_dir()
def test_get_venv_site_packages_dir(tmp_path: Path) -> None:
    """Test get_venv_site_packages_dir return a venv's site-packages dir."""
    fake_venv = tmp_path / ".venv"
    site_pkg_dir = fake_venv / "lib" / "pythonX.Y" / "site-packages"
    site_pkg_dir.mkdir(parents=True)

    result = venv_utils.get_venv_site_packages_dir(fake_venv)

    assert result == site_pkg_dir


def test_get_venv_site_packages_dir_raise(tmp_path: Path) -> None:
    """Test get_venv_site_packages_dir raising exception on no found dir."""
    fake_venv = tmp_path / ".venv"
    fake_venv.mkdir(parents=True)

    with pytest.raises(FileNotFoundError) as excinfo:
        venv_utils.get_venv_site_packages_dir(fake_venv)

    assert "Given venv has no" in str(excinfo.value)


#: Test where_installed()
def test_where_installed_nowhere(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test where_installed with not existing program."""
    monkeypatch.setattr(shutil, "which", lambda _: None)

    result = venv_utils.where_installed("no_existing_program")

    assert result == (0, None, None)


def test_where_installed_only_venv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test where_installed with only global existing program and with venv."""
    fake_glob_bin = tmp_path / "bin"
    #: create fake venv dir
    fake_venv = tmp_path / ".venv"
    monkeypatch.setattr(venv_utils, "get_venv_path", lambda: fake_venv)
    #: create fake exe file
    fake_venv_bin = fake_venv / venv_utils.OS_BIN
    fake_exe = fake_venv_bin / "venv_program"
    #: adjust PATH
    os.environ["PATH"] = str(fake_venv_bin) + os.pathsep + str(fake_glob_bin)
    monkeypatch.setattr(
        venv_utils.shutil, "which", lambda _, path=None: None if path else str(fake_exe)
    )

    result = venv_utils.where_installed("venv_program")

    assert result == (1, str(fake_exe), None)


def test_integr_where_installed_only_venv(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test where_installed with only global existing program and with venv."""
    #: create fake venv dir
    fake_venv = tmp_path / ".venv"
    monkeypatch.setattr(venv_utils, "get_venv_path", lambda: fake_venv)
    #: create fake venv bin dir
    fake_venv_bin = fake_venv / venv_utils.OS_BIN
    fake_venv_bin.mkdir(parents=True)
    #: create fake global bin dir
    fake_glob_bin = tmp_path / "bin"
    fake_glob_bin.mkdir()
    #: create fake exe file
    program = "venv_program" if sys.platform != "win32" else "venv_program.EXE"
    fake_exe = fake_venv_bin / program
    fake_exe.write_text("#!/usr/bin/env python\nprint('hello world')")
    fake_exe.chmod(0o777)
    #: adjust PATH
    os.environ["PATH"] = str(fake_venv_bin) + os.pathsep + str(fake_glob_bin)

    result = venv_utils.where_installed("venv_program")

    assert result == (1, str(fake_exe), None)


def test_where_installed_only_global_no_venv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test where_installed with only global existing program and no venv."""
    monkeypatch.setattr(venv_utils, "get_venv_path", lambda: None)
    #: create fake global bin dir
    fake_glob_bin = tmp_path / "bin"
    #: create fake exe file
    fake_exe = fake_glob_bin / "global_program"
    #: adjust PATH
    os.environ["PATH"] = str(fake_glob_bin)
    monkeypatch.setattr(venv_utils.shutil, "which", lambda _, path=None: str(fake_exe))

    result = venv_utils.where_installed("global_program")

    assert result == (2, None, str(fake_exe))


def test_integr_where_installed_only_global_no_venv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test where_installed with only global existing program and no venv."""
    monkeypatch.setattr(venv_utils, "get_venv_path", lambda: None)
    #: create fake global bin dir
    fake_glob_bin = tmp_path / "bin"
    fake_glob_bin.mkdir()
    #: create fake exe file
    program = "global_program" if sys.platform != "win32" else "global_program.EXE"
    fake_exe = fake_glob_bin / program
    fake_exe.write_text("#!/usr/bin/env python\nprint('hello world')")
    fake_exe.chmod(0o777)
    #: adjust PATH
    os.environ["PATH"] = str(fake_glob_bin)

    result = venv_utils.where_installed("global_program")

    assert result == (2, None, str(fake_exe))


def test_where_installed_only_global_with_venv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test where_installed with only global existing program and with venv."""
    #: create fake venv dir
    fake_venv = tmp_path / ".venv"
    monkeypatch.setattr(venv_utils, "get_venv_path", lambda: fake_venv)
    #: create fake venv bin dir
    fake_venv_bin = fake_venv / venv_utils.OS_BIN
    #: create fake global bin dir
    fake_glob_bin = tmp_path / "bin"
    #: create fake exe file
    fake_exe = fake_glob_bin / "global_program"
    #: adjust PATH
    os.environ["PATH"] = str(fake_venv_bin) + os.pathsep + str(fake_glob_bin)
    monkeypatch.setattr(venv_utils.shutil, "which", lambda _, path=None: str(fake_exe))

    result = venv_utils.where_installed("global_program")

    assert result == (2, None, str(fake_exe))


def test_integr_where_installed_only_global_with_venv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test where_installed with only global existing program and with venv."""
    #: create fake venv dir
    fake_venv = tmp_path / ".venv"
    monkeypatch.setattr(venv_utils, "get_venv_path", lambda: fake_venv)
    #: create fake venv bin dir
    fake_venv_bin = fake_venv / venv_utils.OS_BIN
    fake_venv_bin.mkdir(parents=True)
    #: create fake global bin dir
    fake_glob_bin = tmp_path / "bin"
    fake_glob_bin.mkdir()
    #: create fake exe file
    program = "global_program" if sys.platform != "win32" else "global_program.EXE"
    fake_exe = fake_glob_bin / program
    fake_exe.write_text("#!/usr/bin/env python\nprint('hello world')")
    fake_exe.chmod(0o777)
    #: adjust PATH
    os.environ["PATH"] = str(fake_venv_bin) + os.pathsep + str(fake_glob_bin)

    result = venv_utils.where_installed("global_program")

    assert result == (2, None, str(fake_exe))


def test_where_installed_both(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test where_installed with only global existing program and with venv."""
    #: create fake venv dir
    fake_venv = tmp_path / ".venv"
    monkeypatch.setattr(venv_utils, "get_venv_path", lambda: fake_venv)
    #: create fake venv bin dir
    fake_venv_bin = fake_venv / venv_utils.OS_BIN
    #: create fake exe file in venv bin dir
    venv_fake_exe = fake_venv_bin / "program"
    #: create fake global bin dir
    fake_glob_bin = tmp_path / "bin"
    #: create fake exe file in global bin dir
    glob_fake_exe = fake_glob_bin / "program"
    #: adjust PATH
    os.environ["PATH"] = str(fake_venv_bin) + os.pathsep + str(fake_glob_bin)
    monkeypatch.setattr(
        venv_utils.shutil,
        "which",
        lambda _, path=None: str(glob_fake_exe) if path else str(venv_fake_exe),
    )

    result = venv_utils.where_installed("program")

    assert result == (3, str(venv_fake_exe), str(glob_fake_exe))


def test_integr_where_installed_both(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test where_installed with only global existing program and with venv."""
    #: create fake venv dir
    fake_venv = tmp_path / ".venv"
    monkeypatch.setattr(venv_utils, "get_venv_path", lambda: fake_venv)
    #: create fake venv bin dir
    fake_venv_bin = fake_venv / venv_utils.OS_BIN
    fake_venv_bin.mkdir(parents=True)
    #: create fake exe file in venv bin dir
    program = "program" if sys.platform != "win32" else "program.EXE"
    venv_fake_exe = fake_venv_bin / program
    venv_fake_exe.write_text("#!/usr/bin/env python\nprint('hello world')")
    venv_fake_exe.chmod(0o777)
    #: create fake global bin dir
    fake_glob_bin = tmp_path / "bin"
    fake_glob_bin.mkdir()
    #: create fake exe file in global bin dir
    glob_fake_exe = fake_glob_bin / program
    glob_fake_exe.write_text("#!/usr/bin/env python\nprint('hello world')")
    glob_fake_exe.chmod(0o777)
    #: adjust PATH
    os.environ["PATH"] = str(fake_venv_bin) + os.pathsep + str(fake_glob_bin)

    result = venv_utils.where_installed("program")

    assert result == (3, str(venv_fake_exe), str(glob_fake_exe))
