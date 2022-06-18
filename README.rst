=========================================
 xmltoyml (and ymltoxml) for mavlink xml
=========================================

Some scripts, and eventually a package, to convert real-world XML_ files
to YAML_ and back again, preserving attributes and comments (with minor
corrections).  

Developer workflow
==================

Tool requirements:

* initially just recent Python and Tox_

Both mavlink and pymavlink require a (host) GCC toolchain for full builds,
however, the basic workflow to generate the library headers requires only
Git, Python, and Tox.

.. _Tox: https://github.com/tox-dev/tox
.. _XML: https://en.wikipedia.org/wiki/Extensible_Markup_Language
.. _YAML: https://en.wikipedia.org/wiki/YAML


In-repo workflow with Tox
-------------------------

As long as you have git and at least Python 3.6, then the "easy" dev
workflow is to clone this repository and install Tox via your system
package manager, eg::

  $ sudo apt-get update
  $ sudo apt-get install tox


After cloning the repository, you can run the repo checks with the
``tox`` command.  It will build a virtual python environment with
all the dependencies and run the specified commands, eg:

::

  $ git clone https://github.com/sarnold/ymltoxml
  $ cd ymltoxml/
  $ tox -e py

There is no package yet, just some prototype scripts and a quick test
against one of the mavlink dialect files. The above will run the round-trip
test command using the your (default) system Python; to specify the Python
version and host OS type, run something like::

  $ tox -e py39-linux

Full list of additional ``tox`` commands:

* ``tox -e style`` will run flake8 style checks
* ``tox -e lint`` will run pylint (somewhat less permissive than PEP8/flake8 checks)
* ``tox -e mypy`` will run mypy import and type checking
* ``tox -e isort`` will run isort import checks
* ``tox -e clean`` will remove temporary test files

