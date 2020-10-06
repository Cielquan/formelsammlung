formelsammlung Change Log
=========================
.. note::
  These changes are listed in decreasing version number order and not necessarily chronological.
  Version numbers follow the `SemVer <https://semver.org/>`__ principle.
  See the `tags on this repository <https://github.com/Cielquan/formelsammlung/tags>`__ for all available versions.

  Not all commits are linked. Commits are only linked when they match the specific note.

.. towncrier release notes start

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
