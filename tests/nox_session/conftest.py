"""
    tests.nox_session.conftest
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fixtures for tests for nox_session.

    :copyright: (c) 2020, Christian Riedel and AUTHORS
    :license: GPL-3.0-or-later, see LICENSE for details
"""  # noqa: D205,D208,D400
import sys

import nox.command
import nox.manifest
import nox.registry
import nox.sessions
import nox.virtualenv
import pytest

from nox import _options
from pytest_mock import MockerFixture

from formelsammlung import nox_session


@pytest.fixture
def runner(mocker: MockerFixture) -> nox.sessions.SessionRunner:
    """Create mocked session runner for testing."""
    curr_py_ver = ".".join([str(v) for v in sys.version_info[0:2]])
    func = mocker.Mock(spec=["python"], python=curr_py_ver)
    runner = nox.sessions.SessionRunner(
        name="test",
        signatures=["test"],
        func=func,
        global_config=_options.options.namespace(
            posargs=mocker.sentinel.posargs,
            error_on_external_run=False,
            install_only=False,
        ),
        manifest=mocker.create_autospec(nox.manifest.Manifest),
    )
    runner.venv = mocker.create_autospec(nox.virtualenv.VirtualEnv)
    runner.venv.env = {}  # type: ignore[union-attr]
    runner.venv.bin_paths = ["/dummy/bin/"]  # type: ignore[misc,union-attr]
    return runner


@pytest.fixture
def session(runner: nox.sessions.SessionRunner) -> nox_session.Session:
    """Create mocked session for testing."""
    return nox_session.Session(runner=runner)


@pytest.fixture
def _poetry_installed(monkeypatch) -> None:
    """Mock that poetry is installed."""
    monkeypatch.setattr(nox_session, "where_installed", lambda _: (3, None, None))
