formelsammlung Change Log
=========================
.. note::
  These changes are listed in decreasing version number order and not necessarily chronological.
  Version numbers follow the `SemVer <https://semver.org/>`__ principle.
  See the `tags on this repository <https://github.com/Cielquan/formelsammlung/tags>`__ for all available versions.

.. towncrier release notes start

v0.3.1 (2020-10-24)
-------------------

Bugfixes
~~~~~~~~

- Put `pytest-flask` into `testing` extra, put `flask` into `flask` extra.
  `#16 <https://github.com/Cielquan/formelsammlung/issues/16>`_


Documentation
~~~~~~~~~~~~~

- Removed old "commit mentioning" passage from changelog.
  `#15 <https://github.com/Cielquan/formelsammlung/issues/15>`_


Miscellaneous
~~~~~~~~~~~~~

- Update `flake8-eradicate` to 1.0 in pre-commit.
  `#6 <https://github.com/Cielquan/formelsammlung/issues/6>`_


----


v0.3.0 (2020-10-09)
-------------------

New Features
~~~~~~~~~~~~

- Added autodetection for sphinx doc dir for `SphinxDocServer`.
  `#14 <https://github.com/Cielquan/formelsammlung/issues/14>`_


----


v0.2.1 (2020-10-07)
-------------------

Bugfixes
~~~~~~~~

- Removed redundant dependency python-dotenv.
  `#12 <https://github.com/Cielquan/formelsammlung/issues/12>`_


Documentation
~~~~~~~~~~~~~

- Added instruction for creating a venv to install the packge into to ``installation`` docs.
  `#13 <https://github.com/Cielquan/formelsammlung/issues/13>`_


----


v0.2.0 (2020-10-06)
-------------------

Bugfixes
~~~~~~~~

- Fix the bugged test ``test_strcalc.test_exponentiation`` by increasing the base by one for the negative exponent tests.
  `#5 <https://github.com/Cielquan/formelsammlung/issues/5>`_
- Fixed CI bug with complex numbers.
  `#7 <https://github.com/Cielquan/formelsammlung/issues/7>`_


New Features
~~~~~~~~~~~~

- Added SphinxDocServer. A flask plugin which adds a route to the flask app to show your build sphinx docs.
  `#4 <https://github.com/Cielquan/formelsammlung/issues/4>`_


Documentation
~~~~~~~~~~~~~

- Added missing basic information to docs.
  `#2 <https://github.com/Cielquan/formelsammlung/issues/2>`_
- Added code examples to docstrings.
  `#8 <https://github.com/Cielquan/formelsammlung/issues/8>`_
- Increase toctree depth to 5 to show single submodules in API docs.
  `#9 <https://github.com/Cielquan/formelsammlung/issues/9>`_
- Added little functionality overview to README.
  `#11 <https://github.com/Cielquan/formelsammlung/issues/11>`_


----


v0.1.0 (2020-10-03)
-------------------

Initial release
