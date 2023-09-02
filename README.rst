=========================
 ymltoxml (and xmltoyml)
=========================

|ci| |wheels| |release| |badge|

|pre| |pylint|

|tag| |license| |python|

Python command line tools to convert between XML_ files and YAML_ files,
preserving attributes and comments (with minor corrections).  The default
file encoding for both types is UTF-8 without a BOM. Includes another
console entry point to sort large YAML lists (eg, lists of rules found
in the `SCAP Security Guide`_).

.. _SCAP Security Guide: https://github.com/ComplianceAsCode/content

Quick Start
===========

Install with pip
----------------

This package is *not* yet published on PyPI, thus use one of the following
to install ymltoxml on any platform. Install from the main branch::

  $ https://github.com/sarnold/ymltoxml/archive/refs/heads/main.tar.gz

or use this command to install a specific release version::

  $ pip install https://github.com/sarnold/ymltoxml/releases/download/0.2.2/ymltoxml-0.2.2.tar.gz

The full package provides the ``ymltoxml.py`` executable as well as
a reference configuration file with defaults for all values.

If you'd rather work from the source repository, it supports the common
idiom to install it on your system in a virtual env after cloning::

  $ python3 -m venv env
  $ source env/bin/activate
  $ pip install .
  $ ymltoxml --version
  $ ymltoxml --dump-config
  $ deactivate

The alternative to python venv is the ``tox`` test driver.  If you have it
installed already, see the example tox commands below.

Usage
-----

The current version supports minimal command options; if no options are
provided, the only required arguments are one or more files of a single
type::

  $ ymltoxml
  Usage: ymltoxml [options] arg1 arg2

  Transform YAML to XML and XML to YAML.

  Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -i FILE, --infile=FILE
                          Path to input file (use with --outfile)
    -o FILE, --outfile=FILE
                          Path to output file (use with --infile)
    -v, --verbose         Display more processing info
    -d, --dump-config     Dump default configuration file to stdout


* for processing individual files/paths, use the ``--infile`` option,
  either with or without the ``--outfile`` option
* for processing multiple files, pass all files as arguments (paths
  can be relative or absolute)

  + when passing input files as arguments, the output file names/paths
    are the same as the input files but with the output extension

By default it will process one more input files as command args, typically
in the current directory, however, the ``--infile`` option will only
process a single file path, optionally with an output file path, with no
extra (file) arguments.

The main processing tweaks for yml/xml output formatting are specified
in the default configuration file; if you need to change something, you
can use your own config file in the working directory; note the local
copy must be named ``.ymltoxml.yaml``.  To get a copy of the default
configuration file, do::

  $ cd path/to/work/dir/
  $ ymltoxml --dump-config > .ymltoxml.yaml
  $ $EDITOR .ymltoxml.yaml

An additional helper script is now provided for sorting large (YAML) lists.
The new ``yasort`` script uses its own configuration file, creatively named
``yasort.yaml``. The above applies equally to this new config file.

::
  $ yasort -h
  Usage: yasort [options] arg1 arg2

  Sort YAML lists and write new files.

  Options:
    --version          show program's version number and exit
    -h, --help         show this help message and exit
    -v, --verbose      Display more processing info
    -d, --dump-config  Dump default configuration file to stdout


Features and limitations
------------------------

We only test on mavlink XML message definitions, so it probably *will not*
work at all on arbitrarily complex XML files with namespaces, etc.  The
current round-trip is not exact, due to the following:

* missing encoding is added to version tag
* leading/trailing whitespace in text elements and comments is not preserved
* elements with self-closing tags are converted to full closing tags
* empty elements on more than one line are not preserved

For the files tested (eg, mavlink) the end result is cleaner/shinier XML.

.. note:: This project uses versioningit_ to generate and maintain the
          version file, which only gets included in the sdist/wheel
          packages. In a fresh clone, running any of the tox_ commands
          should generate the current version file.

.. _versioningit: https://github.com/jwodder/versioningit


Dev workflows
=============

The following covers two types of workflows, one for tool usage in other
(external) projects, and one for (internal) tool development.

Mavlink support
---------------

The ymltoxml tool is intended to be part of larger workflow, ie, developing
custom mavlink message dialects and generating/deploying the resulting
mavlink language interfaces.  To be more specific, for this example we
use a mavlink-compatible component running on a micro-controller, thus
the target language bindings are C and C++.

Tool requirements for the full mavlink workflow:

* initially just recent pymavlink, Python, and Tox_

Both mavlink and pymavlink require a (host) GCC toolchain for full builds,
however, the basic workflow to generate mavlink library headers requires
only Git, Python, and Tox.

.. _mavlink: https://mavlink.io/en/messages/common.html
.. _Tox: https://github.com/tox-dev/tox
.. _XML: https://en.wikipedia.org/wiki/Extensible_Markup_Language
.. _YAML: https://en.wikipedia.org/wiki/YAML

SCAP support
------------

The yasort tool is also intended to be part of a larger workflow, mainly
working with SCAP content, ie, the scap-security-guide source files (or
just content_). It is currently used to sort profiles with large numbers
of rules to make it easier to visually diff and spot duplicates, etc.

The configuration file defaults are based on existing yaml structure, but
you are free to change them for another use case. To adjust how the sorting
works, make a local config file (see above) and edit as needed the following
options:

:output_dirname: directory for output file(s)
:default_parent_key: parent key if sort target is sublist
:default_sort_key: the key you want to sort
:has_parent_key: set true if sorting a sublist
:default_yml_ext: change the output file extension

The rest of the options are for YAML formatting/flow style (see the ruamel_
documetation for formatting details)

.. _content: https://complianceascode.readthedocs.io/en/latest/
.. _ruamel: https://yaml.readthedocs.io/en/latest/

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

* ``tox -e dev`` pip "developer" install
* ``tox -e style`` will run flake8 style checks
* ``tox -e lint`` will run pylint (somewhat less permissive than PEP8/flake8 checks)
* ``tox -e mypy`` will run mypy import and type checking
* ``tox -e isort`` will run isort import checks
* ``tox -e clean`` will remove temporary test files

To build/lint the api docs, use the following tox commands:

* ``tox -e docs`` build the documentation using sphinx and the api-doc plugin
* ``tox -e docs-lint`` build the docs and run the sphinx link checking


Making Changes & Contributing
=============================

We use the gitchangelog_ action to generate our github Release page, as
well as the gitchangelog message format to help it categorize/filter
commits for a tidier release page. Please use the appropriate ACTION
modifiers in any Pull Requests.

This repo is also pre-commit_ enabled for various linting and format
checks.  The checks run automatically on commit and will fail the
commit (if not clean) with some checks performing simple file corrections.

If other checks fail on commit, the failure display should explain the error
types and line numbers. Note you must fix any fatal errors for the
commit to succeed; some errors should be fixed automatically (use
``git status`` and ``git diff`` to review any changes).

See the following pages for more information on gitchangelog and pre-commit.

.. inclusion-marker-1

* generate-changelog_
* pre-commit-config_
* pre-commit-usage_

.. _generate-changelog:  docs/source/dev/generate-changelog.rst
.. _pre-commit-config: docs/source/dev/pre-commit-config.rst
.. _pre-commit-usage: docs/source/dev/pre-commit-usage.rst
.. inclusion-marker-2

You will need to install pre-commit before contributing any changes;
installing it using your system's package manager is recommended,
otherwise install with pip into your usual virtual environment using
something like::

  $ sudo emerge pre-commit  --or--
  $ pip install pre-commit

then install it into the repo you just cloned::

  $ git clone https://github.com/sarnold/ymltoxml
  $ cd ymltoxml/
  $ pre-commit install

It's usually a good idea to update the hooks to the latest version::

    pre-commit autoupdate


.. _gitchangelog: https://github.com/sarnold/gitchangelog-action
.. _pre-commit: http://pre-commit.com/


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

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
