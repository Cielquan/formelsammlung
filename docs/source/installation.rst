Installation
============

This part of the documentation covers how to install the package.
It is recommended to install the package in a virtual environment.


Create virtual environment
--------------------------
There are several packages/modules for creating python virtual environments.
You are free to use which you want. Here I use ``venv`` because it is build in::

    $ python -m venv venv

After creation activate the `venv` to work with it (Linux)::

    $ source venv/bin/activate

.. highlight:: default

On windows machines call instead::

    > venv\Scripts\activate

.. highlight:: console

Installation from PyPI
----------------------
``formelsammlung`` is published on PyPI so you can simply install it with :command:`pip`::

    $ pip install formelsammlung


Installation from source
------------------------
``formelsammlung`` can also be install directly from a clone of the `Git repository`__.
You can either clone the repo and install the local clone::

    $ git clone https://github.com/Cielquan/formelsammlung.git
    $ cd formelsammlung
    $ pip install .

or install it directly via :command:`git`::

    $ pip install git+https://github.com/Cielquan/formelsammlung.git

You can also grab the repo in either `tar.gz`__ or `zip`__ format.
After downloading and extracting you can install it with :command:`pip` like above.


.. highlight:: default


__ https://github.com/Cielquan/formelsammlung
__ https://github.com/Cielquan/formelsammlung/archive/master.tar.gz
__ https://github.com/Cielquan/formelsammlung/archive/master.zip
