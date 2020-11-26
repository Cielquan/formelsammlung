"""
    formelsammlung.tox_env_exe_runner
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Call tools from tox environments.

    :copyright: 2020 (c) Christian Riedel
    :license: GPLv3, see LICENSE file for more details
"""  # noqa: D205, D208, D400
import subprocess  # nosec
import sys

from pathlib import Path
from typing import List, Optional


def env_exe_runner(  # pylint: disable=R0912
    venv_runner: List[str],
    envs: List[str],
    tool: str,
    tool_args: Optional[List[str]] = None,
) -> int:
    """Call given ``tool`` from given `tox` or `nox` or `virtual` env considering OS.

    :param venv_runner: 'nox' and/or 'tox' and/or a 'virtual environment'
    :param envs: List of environments to search the ``tool`` in when 'tox' or 'nox' is
        in venv_runner.
    :param tool: Name of the executable to run.
    :param tool_args: Arguments to give to the ``tool``.
    :return: Exit code 127 if no executable is found or the exit code of the called cmd.
    """
    is_win = sys.platform == "win32"

    exe = Path(f"Scripts/{tool}.exe") if is_win else Path(f"bin/{tool}")
    cmd = None

    if not tool_args:
        tool_args = []

    for runner in venv_runner:
        if runner in ("tox", "nox"):
            for env in envs:
                path = Path(f".{runner}") / env / exe
                if path.is_file():
                    cmd = (str(path), *tool_args)
                    break
        else:
            path = Path(runner) / exe
            if path.is_file():
                cmd = (str(path), *tool_args)
        if cmd:
            break

    if cmd is None:
        print(f"No '{tool}' executable found. Search in:")
        for runner in venv_runner:
            if runner == "tox":
                print(f"- 'tox' envs: {envs}")
            elif runner == "nox":
                print(f"- 'nox' envs: {envs}")
            else:
                print(f"- virtual env: ['{runner}']")
        return 127

    return subprocess.call(cmd)  # nosec


def cli_caller() -> int:
    """Warp ``env_exe_runner`` to be callable by cli.

    Script to call executables in `tox`/`nox` envs considering OS.

    The script takes two mandatory arguments:

    1. The runner managing the env: `tox` or `nox`.
    2. A string with comma separated `tox`/`nox` envs to check for the executable.
       The envs are checked in given order.
    3. The executable to call like e.g. `pylint`.

    All other arguments after are passed to the tool on call.

    :return: Exit code from ``env_exe_runner``
    """
    return env_exe_runner(
        sys.argv[1].split(","), sys.argv[2].split(","), sys.argv[3], sys.argv[4:]
    )  # pragma: no cover


if __name__ == "__main__":
    sys.exit(cli_caller())
