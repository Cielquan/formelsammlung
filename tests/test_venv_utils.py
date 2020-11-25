"""
    tests.test_venv_utils
    ~~~~~~~~~~~~~~~~~~~~~

    Tests for venv_utils.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""  # noqa: D205,D208,D400
import os
import shutil
import sys
import formelsammlung.venv_utils as vu


def test_get_venv_path_w_real_prefix(monkeypatch):
    """Test get_venv_path return when sys.real_prefix is set."""
    sys.real_prefix = ""
    monkeypatch.setattr(sys, "real_prefix", "path-to-venv-via-real_prefix")

    result = vu.get_venv_path()

    assert result == "path-to-venv-via-real_prefix"


def test_get_venv_path_w_prefix(monkeypatch):
    """Test get_venv_path return when sys.real_prefix is not set."""
    monkeypatch.delattr(sys, "real_prefix", raising=False)
    monkeypatch.setattr(sys, "prefix", "path-to-venv-via-prefix")

    result = vu.get_venv_path()

    assert result == "path-to-venv-via-prefix"


def test_get_venv_path_no_venv(monkeypatch):
    """Test get_venv_path return when no venv is used."""
    monkeypatch.delattr(sys, "real_prefix", raising=False)
    monkeypatch.setattr(sys, "prefix", sys.base_prefix)

    result = vu.get_venv_path()

    assert result == None


def test_get_venv_site_packages_dir(tmp_path):
    """Test get_venv_site_packages_dir return a venv's site-packages dir."""
    fake_venv = tmp_path / ".venv"
    site_pkg_dir = fake_venv / "lib" / "pythonX.Y" / "site-packages"
    site_pkg_dir.mkdir(parents=True)

    result = vu.get_venv_site_packages_dir(fake_venv)

    assert result == site_pkg_dir


def test_where_installed_nowhere(monkeypatch):
    """Test where_installed with not existing program."""
    monkeypatch.setattr(shutil, "which", lambda _: None)

    result = vu.where_installed("no_existing_program")

    assert result == (0, None, None)


def test_where_installed_only_venv(tmp_path, monkeypatch):
    """Test where_installed with only global existing program and with venv."""
    fake_venv = tmp_path / ".venv"
    monkeypatch.setattr(vu, "get_venv_path", lambda: str(fake_venv))

    fake_venv_bin = fake_venv / ("Scripts" if sys.platform == "win32" else "bin")
    fake_venv_bin.mkdir(parents=True)

    fake_glob_bin = tmp_path / "bin"
    fake_glob_bin.mkdir()

    fake_exe = fake_venv_bin / "venv_program"
    fake_exe.write_text("# just a fake exe")
    fake_exe.chmod(0o777)

    os.environ = {"PATH": str(fake_venv_bin) + os.pathsep + str(fake_glob_bin)}

    result = vu.where_installed("venv_program")

    assert result == (1, str(fake_exe), None)


def test_where_installed_only_global_no_venv(tmp_path, monkeypatch):
    """Test where_installed with only global existing program and no venv."""
    monkeypatch.setattr(vu, "get_venv_path", lambda : None)

    fake_glob_bin = tmp_path / "bin"
    fake_glob_bin.mkdir()

    fake_exe = fake_glob_bin / "global_program"
    fake_exe.write_text("# just a fake exe")
    fake_exe.chmod(0o777)

    os.environ = {"PATH": str(fake_glob_bin)}

    result = vu.where_installed("global_program")

    assert result == (2, None, str(fake_exe))


def test_where_installed_only_global_with_venv(tmp_path, monkeypatch):
    """Test where_installed with only global existing program and with venv."""
    fake_venv = tmp_path / ".venv"
    monkeypatch.setattr(vu, "get_venv_path", lambda: str(fake_venv))

    fake_venv_bin = fake_venv / ("Scripts" if sys.platform == "win32" else "bin")
    fake_venv_bin.mkdir(parents=True)

    fake_glob_bin = tmp_path / "bin"
    fake_glob_bin.mkdir()

    fake_exe = fake_glob_bin / "global_program"
    fake_exe.write_text("# just a fake exe")
    fake_exe.chmod(0o777)

    os.environ = {"PATH": str(fake_venv_bin) + os.pathsep + str(fake_glob_bin)}

    result = vu.where_installed("global_program")

    assert result == (2, None, str(fake_exe))


def test_where_installed_both(tmp_path, monkeypatch):
    """Test where_installed with only global existing program and with venv."""
    fake_venv = tmp_path / ".venv"
    monkeypatch.setattr(vu, "get_venv_path", lambda: str(fake_venv))

    fake_venv_bin = fake_venv / ("Scripts" if sys.platform == "win32" else "bin")
    fake_venv_bin.mkdir(parents=True)

    venv_fake_exe = fake_venv_bin / "program"
    venv_fake_exe.write_text("# just a fake exe")
    venv_fake_exe.chmod(0o777)

    fake_glob_bin = tmp_path / "bin"
    fake_glob_bin.mkdir()

    glob_fake_exe = fake_glob_bin / "program"
    glob_fake_exe.write_text("# just a fake exe")
    glob_fake_exe.chmod(0o777)

    os.environ = {"PATH": str(fake_venv_bin) + os.pathsep + str(fake_glob_bin)}

    result = vu.where_installed("program")

    assert result == (3, str(venv_fake_exe), str(glob_fake_exe))
