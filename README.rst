=========================================
 ymltoxml (and xmltoyml) for mavlink xml
=========================================

|ci| |wheels| |release| |badge|

|pylint|

|tag| |license| |python|

A Python command line tool to convert between XML_ files and YAML_ files,
preserving attributes and comments (with minor corrections).  The default
file encoding for both types is UTF-8 without a BOM.  The main intent is
to support YAML-based development of custom mavlink_ dialects.

Local workflow
===============

Tool requirements:

* initially just recent Python and Tox_

Both mavlink and pymavlink require a (host) GCC toolchain for full builds,
however, the basic workflow to generate mavlink library headers requires
only Git, Python, and Tox.

.. _mavlink: https://mavlink.io/en/messages/common.html
.. _Tox: https://github.com/tox-dev/tox
.. _XML: https://en.wikipedia.org/wiki/Extensible_Markup_Language
.. _YAML: https://en.wikipedia.org/wiki/YAML

.. note:: This project uses versioningit_ to generate and maintain the
          version file, which only gets included in the sdist/wheel
          packages. In a fresh clone, running any of the tox_ commands
          should generate the current version file.

.. _versioningit: https://github.com/jwodder/versioningit


In-repo workflow with Tox
-------------------------

As long as you have git and at least Python 3.6, then the "easy" dev
workflow is to clone this repository and install Tox via your system
package manager, eg::

  $ sudo apt-get update
  $ sudo apt-get install tox


After cloning this repository, you can run the repo checks with the
``tox`` command.  It will build a virtual python environment with
all the dependencies and run the specified commands, eg:

::

  $ git clone https://github.com/sarnold/ymltoxml
  $ cd ymltoxml/
  $ tox -e py

There are no actual unittests yet, but the above will run the base ``tox``
command against one of the mavlink dialect files. Note this will run the
round-trip test command using the your (default) system Python; to specify
the Python version and host OS type, run something like::

  $ tox -e py39-linux

Full list of additional ``tox`` commands:

* ``tox -e style`` will run flake8 style checks
* ``tox -e lint`` will run pylint (somewhat less permissive than PEP8/flake8 checks)
* ``tox -e mypy`` will run mypy import and type checking
* ``tox -e isort`` will run isort import checks
* ``tox -e clean`` will remove temporary test files

To build/lint the api docs, use the following tox commands:

* ``tox -e docs`` build the documentation using sphinx and the api-doc plugin
* ``tox -e docs-lint`` build the docs and run the sphinx link checking


.. |ci| image:: https://github.com/sarnold/ymltoxml/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/sarnold/ymltoxml/actions/workflows/ci.yml
    :alt: CI Status

.. |wheels| image:: https://github.com/sarnold/ymltoxml/actions/workflows/wheels.yml/badge.svg
    :target: https://github.com/sarnold/ymltoxml/actions/workflows/wheels.yml
    :alt: Wheel Status

.. |badge| image:: https://github.com/sarnold/ymltoxml/actions/workflows/pylint.yml/badge.svg
    :target: https://github.com/sarnold/ymltoxml/actions/workflows/pylint.yml
    :alt: Pylint Status

.. |release| image:: https://github.com/sarnold/ymltoxml/actions/workflows/release.yml/badge.svg
    :target: https://github.com/sarnold/ymltoxml/actions/workflows/release.yml
    :alt: Release Status

.. |pylint| image:: https://raw.githubusercontent.com/sarnold/ymltoxml/badges/main/pylint-score.svg
    :target: https://github.com/sarnold/ymltoxml/actions/workflows/pylint.yml
    :alt: Pylint score

.. |license| image:: https://img.shields.io/github/license/sarnold/ymltoxml
    :target: https://github.com/sarnold/ymltoxml/blob/master/LICENSE
    :alt: License

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/ymltoxml?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/ymltoxml/releases
    :alt: GitHub tag

.. |python| image:: https://img.shields.io/badge/python-3.6+-blue.svg
    :target: https://www.python.org/downloads/
    :alt: Python
