"""
    tests.nox_session.test__nox_session
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for nox_session.py.

    :copyright: (c) Christian Riedel
    :license: GPLv3
"""  # noqa: D205,D208,D400
#: Tests are based on:
#: https://github.com/theacodes/nox/blob/156765c343942233bf6cbfa59391ec63d6fedc29/tests/test_sessions.py  # noqa: E501
import nox.command
import nox.manifest
import nox.registry
import nox.sessions
import nox.virtualenv
import pytest

from pytest_mock import MockerFixture

from formelsammlung import nox_session


NoneType = type(None)


@pytest.mark.usefixtures("_poetry_installed")
def test_poetry_install(session: nox_session.Session, mocker: MockerFixture) -> None:
    """Test argumentless call."""
    run = mocker.patch.object(session, "_run", autospec=True)
    session.poetry_install()
    run.assert_called_once_with(
        "poetry",
        "install",
        silent=True,
        external="error",
    )


@pytest.mark.usefixtures("_poetry_installed")
def test_poetry_install_w_extras(
    session: nox_session.Session, mocker: MockerFixture
) -> None:
    """Test call with extras specified."""
    run = mocker.patch.object(session, "_run", autospec=True)
    session.poetry_install("extra1 extra2")
    run.assert_called_once_with(
        "poetry",
        "install",
        "--extras",
        "extra1 extra2",
        silent=mocker.ANY,
        external=mocker.ANY,
    )


@pytest.mark.usefixtures("_poetry_installed")
def test_poetry_install_w_nono_flags(
    session: nox_session.Session, mocker: MockerFixture
) -> None:
    """Test call no_root and no_dev."""
    run = mocker.patch.object(session, "_run", autospec=True)
    session.poetry_install(no_root=True, no_dev=True)
    run.assert_called_once_with(
        "poetry",
        "install",
        "--no-root",
        "--no-dev",
        silent=mocker.ANY,
        external=mocker.ANY,
    )


@pytest.mark.usefixtures("_poetry_installed")
def test_poetry_install_w_all_install_args(
    session: nox_session.Session, mocker: MockerFixture
) -> None:
    """Test call extras and no_root and no_dev."""
    run = mocker.patch.object(session, "_run", autospec=True)
    session.poetry_install("extra1 extra2", no_root=True, no_dev=True)
    run.assert_called_once_with(
        "poetry",
        "install",
        "--no-root",
        "--no-dev",
        "--extras",
        "extra1 extra2",
        silent=mocker.ANY,
        external=mocker.ANY,
    )


@pytest.mark.usefixtures("_poetry_installed")
def test_poetry_install_not_a_virtualenv(
    session: nox_session.Session, runner: nox.sessions.SessionRunner
) -> None:
    """Test ValueError is risen when no venv is set."""
    runner.venv = None

    with pytest.raises(ValueError, match="w/o a virtualenv"):
        session.poetry_install()


@pytest.mark.usefixtures("_poetry_installed")
def test_poetry_install_non_default_kwargs(
    session: nox_session.Session, mocker: MockerFixture
) -> None:
    """Test call of non default kwargs."""
    run = mocker.patch.object(session, "_run", autospec=True)
    session.poetry_install(silent=False)
    run.assert_called_once_with(
        "poetry",
        "install",
        silent=False,
        external="error",
    )


@pytest.mark.usefixtures("_poetry_installed")
def test_poetry_install_pip_require_venv_false(
    session: nox_session.Session, mocker: MockerFixture
) -> None:
    """Test call with pip_require_venv False."""
    run = mocker.patch.object(nox.command, "run")
    session.poetry_install()
    run.assert_called_once_with(
        ("poetry", "install"),
        env={},
        silent=mocker.ANY,
        external=mocker.ANY,
        paths=mocker.ANY,
    )


@pytest.mark.usefixtures("_poetry_installed")
def test_poetry_install_pip_require_venv_true(
    session: nox_session.Session, mocker: MockerFixture
) -> None:
    """Test call with pip_require_venv False."""
    run = mocker.patch.object(nox.command, "run")
    session.poetry_install(pip_require_venv=True)
    run.assert_called_once_with(
        ("poetry", "install"),
        env={"PIP_REQUIRE_VIRTUALENV": "true"},
        silent=mocker.ANY,
        external=mocker.ANY,
        paths=mocker.ANY,
    )


@pytest.mark.usefixtures("_poetry_installed")
def test_poetry_install_pip_require_venv_true_w_env_set(
    session: nox_session.Session, mocker: MockerFixture
) -> None:
    """Test call with pip_require_venv False and kwarg env set."""
    run = mocker.patch.object(nox.command, "run")
    session.poetry_install(pip_require_venv=True, env={"TEST": "success"})
    run.assert_called_once_with(
        ("poetry", "install"),
        env={"TEST": "success", "PIP_REQUIRE_VIRTUALENV": "true"},
        silent=mocker.ANY,
        external=mocker.ANY,
        paths=mocker.ANY,
    )


def test_poetry_install_install_missing_poetry(
    session: nox_session.Session, mocker: MockerFixture
) -> None:
    """Test call with missing poetry executable."""
    mocker.patch.object(nox_session, "where_installed", return_value=(0, None, None))
    run = mocker.patch.object(nox.command, "run")
    session.poetry_install()
    calls = [
        mocker.call(
            ("python", "-m", "pip", "install", "poetry>=1"),
            env={"PIP_DISABLE_VERSION_CHECK": "1"},
            silent=mocker.ANY,
            external=mocker.ANY,
            paths=mocker.ANY,
        ),
        mocker.call(
            ("poetry", "install"),
            env=mocker.ANY,
            silent=mocker.ANY,
            external=mocker.ANY,
            paths=mocker.ANY,
        ),
    ]
    run.assert_has_calls(calls)


@pytest.mark.usefixtures("_poetry_installed")
def test_run_install_only_should_install(
    session: nox_session.Session,
    runner: nox.sessions.SessionRunner,
    mocker: MockerFixture,
) -> None:
    """Test poetry_install run when `install_only` is True."""
    runner.global_config.install_only = True

    run = mocker.patch.object(nox.command, "run")
    session.poetry_install("spam")
    session.run("spam", "eggs")

    run.assert_called_once_with(
        ("poetry", "install", "--extras", "spam"),
        env=mocker.ANY,
        external=mocker.ANY,
        paths=mocker.ANY,
        silent=mocker.ANY,
    )


def test_session_w_poetry_decorator_name_overwrite() -> None:
    """Test if decorator takes decorated functions name and docstring."""
    def testing_func() -> None:
        """Test docstr."""
        pass
    deco_func = nox_session.session_w_poetry(testing_func)

    assert deco_func.__name__ == testing_func.__name__
    assert deco_func.__doc__ == testing_func.__doc__


def test_session_w_poetry_decorator_session_change(runner: nox.sessions.SessionRunner, mocker: MockerFixture) -> None:
    """Test if decorator changes session class."""
    mocker.patch.object(nox.command, "run")

    @nox.session
    def testing_func_default(session: nox.sessions.Session) -> None:
        """Test docstr."""
        assert isinstance(session, nox.sessions.Session)
        assert not isinstance(session, nox_session.Session)

    testing_func_default(nox.sessions.Session(runner))

    @nox.session
    @nox_session.session_w_poetry
    def testing_func_changed(session: nox_session.Session) -> None:
        """Test docstr."""
        assert isinstance(session, nox.sessions.Session)
        assert isinstance(session, nox_session.Session)

    testing_func_changed(nox.sessions.Session(runner))
