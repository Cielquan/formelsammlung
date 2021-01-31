# Changelog

This is the changelog of `formelsammlung`. Releases and their respective
changes are listed here. The order of releases is time and **not** version based!
For a list of all available releases see the
[release section on Github](https://github.com/Cielquan/formelsammlung/releases).


<!-- Valid subcategories
#### BREAKING CHANGES
#### New features
#### Bugfixes
#### Documentation
#### Miscellaneous
-->


## Unreleased
[diff v3.2.0...main](https://github.com/Cielquan/formelsammlung/compare/v3.2.0...main)

#### BREAKING CHANGES
- `strcalc.calculate_string` now raises `strcalc.StringCalculatorError` exceptions

#### New features

- added `nox_session.session_w_poetry` decorator for use in noxfile.py.
- updated root `__init__.py` to serve more metadata.

#### Bugfixes

- fixed constructor of `flask_sphinx_docs.SphinxDocServer` to take the right arguments
- fixed type hints `flask_sphinx_docs`
- fixed `SphinxDocServer.web_docs`'s (view function) way of patching the
  `app.static_folder`.

#### Miscellaneous

- moved CI to Github Actions
- added Github templates
- updated dev tools and repo structure to match my new *standard*



## [v3.2.0](https://github.com/Cielquan/formelsammlung/releases/v3.2.0) (2021-01-21)
[diff v3.1.0...v3.2.0](https://github.com/Cielquan/formelsammlung/compare/v3.1.0...v3.2.0)

#### New features

- `get_venv_tmp_dir` now take a tuple of temp dir names to search (optional).
- `get_venv_tmp_dir` now can create a temp dir if non is found (opt-in). The name of
  the temp dir can be customized.



## [v3.1.0](https://github.com/Cielquan/formelsammlung/releases/v3.1.0) (2021-01-21)
[diff 3.0.1...v3.1.0](https://github.com/Cielquan/formelsammlung/compare/3.0.1...v3.1.0)

#### New features

- `get_venv_tmp_dir` now also finds dotted tmp directories.

#### Bugfixes:

- `test_exponentiation` no allows 0 for first number, which caused `ZeroDivisionError`.



## [v3.0.1](https://github.com/Cielquan/formelsammlung/releases/3.0.1) (2020-12-11)
[diff 3.0.0...3.0.1](https://github.com/Cielquan/formelsammlung/compare/3.0.0...3.0.1)

#### Bugfixes:

- `where_installed` no longer fails when no venv is active.



## [v3.0.0](https://github.com/Cielquan/formelsammlung/releases/3.0.0) (2020-12-07)
[diff 2.0.0...3.0.0](https://github.com/Cielquan/formelsammlung/compare/2.0.0...3.0.0)

#### BREAKING CHANGES

- `get_venv_path`, `get_venv_bin_dir`, `get_venv_tmp_dir` and
  `get_venv_site_packages_dir` now always raise `FileNotFoundError` when a venv or
  the corresponding directory could not be found. Removed the `raises_error` parameter.



## [v2.0.0](https://github.com/Cielquan/formelsammlung/releases/2.0.0) (2020-12-07)
[diff 1.2.0...2.0.0](https://github.com/Cielquan/formelsammlung/compare/1.2.0...2.0.0)

#### New features

- Added `get_venv_bin_dir` and `get_venv_tmp_dir` functions.

#### BREAKING CHANGES

- `get_venv_path` now returns a `pathlib.Path` object instead of a string.



## [v1.2.0](https://github.com/Cielquan/formelsammlung/releases/1.2.0) (2020-11-26)
[diff 1.1.0...1.2.0](https://github.com/Cielquan/formelsammlung/compare/1.1.0...1.2.0)

#### New features

- `env_exe_runner` now takes a list of runners which can also be a venv.



## [v1.1.0](https://github.com/Cielquan/formelsammlung/releases/1.1.0) (2020-11-25)
[diff 1.0.0...1.1.0](https://github.com/Cielquan/formelsammlung/compare/1.0.0...1.1.0)

#### New features

- Added `venv_utils` module.



## [v1.0.0](https://github.com/Cielquan/formelsammlung/releases/1.0.0) (2020-11-21)
[diff 0.4.0...1.0.0](https://github.com/Cielquan/formelsammlung/compare/0.4.0...1.0.0)

#### BREAKING CHANGES

- Renamed `tox_env_exe_runner` to `env_exe_runner` and added `runner` argument
  on 2nd place, which takes either `tox` or `nox`. With this both runner are supported.



## [v0.4.0](https://github.com/Cielquan/formelsammlung/releases/0.4.0) (2020-11-14)
[diff 0.3.2...0.4.0](https://github.com/Cielquan/formelsammlung/compare/0.3.2...0.4.0)

#### New features

- Added tox_env_exe_runner with wrapper to call it from cli.
  [#17](https://github.com/Cielquan/formelsammlung/issues/17)



## [v0.3.2](https://github.com/Cielquan/formelsammlung/releases/0.3.2) (2020-11-13)
[diff 0.3.1...0.3.2](https://github.com/Cielquan/formelsammlung/compare/0.3.1...0.3.2)

#### Miscellaneous

- Broaden importlib-metadata version dependency



## [v0.3.1](https://github.com/Cielquan/formelsammlung/releases/0.3.1) (2020-10-24)
[diff 0.3.0...0.3.1](https://github.com/Cielquan/formelsammlung/compare/0.3.0...0.3.1)

#### Bugfixes:

- Put `pytest-flask` into `testing` extra, put `flask` into `flask` extra.
  [#16](https://github.com/Cielquan/formelsammlung/issues/16)

#### Documentation

- Removed old "commit mentioning" passage from changelog.
  [#15](https://github.com/Cielquan/formelsammlung/issues/15)

#### Miscellaneous

- Update `flake8-eradicate` to 1.0 in pre-commit.
  [#6](https://github.com/Cielquan/formelsammlung/issues/6)



## [v0.3.0](https://github.com/Cielquan/formelsammlung/releases/0.3.0) (2020-10-09)
[diff 0.2.1...0.3.0](https://github.com/Cielquan/formelsammlung/compare/0.2.1...0.3.0)

#### New features

- Added auto detection for sphinx doc dir for `SphinxDocServer`.
  [#14](https://github.com/Cielquan/formelsammlung/issues/14)



## [v0.2.1](https://github.com/Cielquan/formelsammlung/releases/0.2.1) (2020-10-07)
[diff 0.2.0...0.2.1](https://github.com/Cielquan/formelsammlung/compare/0.2.0...0.2.1)

#### Bugfixes:

- Removed redundant dependency python-dotenv.
  [#12](https://github.com/Cielquan/formelsammlung/issues/12)

#### Documentation

- Added instruction for creating a venv to install the package into to `installation` docs.
  [#13](https://github.com/Cielquan/formelsammlung/issues/13)



## [v0.2.0](https://github.com/Cielquan/formelsammlung/releases/0.2.0) (2020-10-06)
[diff 0.1.0...0.2.0](https://github.com/Cielquan/formelsammlung/compare/0.1.0...0.2.0)

#### Bugfixes:

- Fix the bugged test `test_strcalc.test_exponentiation` by increasing the base by one for the negative exponent tests.
  [#5](https://github.com/Cielquan/formelsammlung/issues/5)
- Fixed CI bug with complex numbers.
  [#7](https://github.com/Cielquan/formelsammlung/issues/7)

#### New features

- Added SphinxDocServer. A flask plugin which adds a route to the flask app to show your build sphinx docs.
  [#4](https://github.com/Cielquan/formelsammlung/issues/4)

#### Documentation

- Added missing basic information to docs.
  [#2](https://github.com/Cielquan/formelsammlung/issues/2)
- Added code examples to docstrings.
  [#8](https://github.com/Cielquan/formelsammlung/issues/8)
- Increase toctree depth to 5 to show single submodules in API docs.
  [#9](https://github.com/Cielquan/formelsammlung/issues/9)
- Added little functionality overview to README.
  [#11](https://github.com/Cielquan/formelsammlung/issues/11)



## [v0.1.0](https://github.com/Cielquan/formelsammlung/releases/0.1.0) (2020-10-03)
[diff 99e898760f82ce5da674ce02343c6ddb84ba179c...0.1.0](https://github.com/Cielquan/formelsammlung/compare/99e898760f82ce5da674ce02343c6ddb84ba179c...0.1.0)

Initial release
