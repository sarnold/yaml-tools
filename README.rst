=======================================
 yaml-tools (and more for CSV and XML)
=======================================

|ci| |wheels| |release| |badge| |coverage|

|pre| |reuse| |cov| |pylint|

|tag| |license| |python| |contributors|

Python command line tools for working with YAML and similar structured
text data, eg, round-trip conversion between XML_ and YAML_, preserving
attributes and comments (with minor corrections).  The default file
encoding for all types is UTF-8 without a BOM. Now includes more
console entry points to grep or sort interesting YAML files (eg, lists
of rules found in the `SCAP Security Guide`_) and support for more
input file types to ingest SSG and other upstream data, eg, NIST
oscal-content_.

.. _SCAP Security Guide: https://github.com/ComplianceAsCode/content
.. _oscal-content: https://github.com/usnistgov/oscal-content

Quick Start
===========

Available modules, console commands, and scripts:

* ``ymltoxml`` - YAML / XML round-trip conversion and cleanup
* ``yasort`` - sort large lists in YAML files
* ``yagrep`` - grep for keys/values in YAML files
* ``oscal`` (*WIP*) - ingest NIST 800-53 content in multiple formats

Experimental "demo" scripts:

* ``analyze_control_ids.py`` - analyze control ID sets with optional fuzzy match
* ``analyze_ssg_controls.py`` - analyze NIST controls from SSG content

For the above "demo" scripts, check the top of the source file for any knobs
adjustable via environment variables, eg:

.. code-block:: python

  FILE = os.getenv(
      "ID_FILE",
      default="tests/data/OE-expanded-profile-all-ids.txt",
  )
  SSG_PATH = os.getenv("SSG_PATH", default="ext/content/controls")
  DEBUG = int(os.getenv("DEBUG", default=0))


.. note:: Text files with a single "column" of IDs have a special read mode
          but the files must be named with the string "ids" in the filename
          and the extension ".txt" for this mode to be used (as in the example
          above).


Install with pip
----------------

This package is *not* yet published on PyPI, thus use one of the following
to install yaml-tools on any platform. Install from the main branch::

  $ pip install https://github.com/sarnold/yaml-tools/archive/refs/heads/main.tar.gz

or use this command to install a specific release version::

  $ pip install https://github.com/sarnold/yaml-tools/releases/download/0.4.0/yaml_tools-0.4.0.tar.gz

The ``yaml_tools`` package provides the modules shown above as well as
module-specific reference configuration files with defaults for all values.

If you'd rather work from the source repository, it supports the common
idiom to install it on your system in a virtual env after cloning::

  $ python3 -m venv env
  $ source env/bin/activate
  (env) $ pip install .
  (env) $ ymltoxml --version
  (env) $ ymltoxml --dump-config
  (env) $ deactivate

The alternative to python venv is the ``tox`` test driver.  If you have it
installed already, see the example tox commands below.

ymltoxml
--------

The current version supports minimal command options; if no options are
provided, the only required arguments are one or more files of a single
type::

  $ ymltoxml
  usage: ymltoxml [-h] [--version] [-v] [-d] [-s] [-i [FILE]] [-o [FILE]]
                  [FILE ...]

  Transform YAML to XML and XML to YAML

  positional arguments:
    FILE                  Process input file(s) to target extension (default:
                          None)

  options:
    -h, --help            show this help message and exit
    --version             show program's version number and exit
    -v, --verbose         Display more processing info (default: False)
    -d, --dump-config     Dump default configuration file to stdout (default:
                          False)
    -s, --save-config     save active config to default filename (.ymltoxml.yml)
                          and exit (default: False)
    -i [FILE], --infile [FILE]
                          Path to single input file (use with --outfile)
                          (default: None)
    -o [FILE], --outfile [FILE]
                          Path to single output file (use with --infile)
                          (default: None)

* for processing individual files/paths, use the ``--infile`` option,
  either with or without the ``--outfile`` option
* for processing multiple files, pass all files as arguments (paths
  can be relative or absolute)

  + when passing input files as arguments, the output file names/paths
    are the same as the input files but with the (new) output extension

By default it will process one or more input files as command args, typically
in the current directory, however, the ``--infile`` option will only
process a single file path, optionally with an output file path, with no
extra (file) arguments.

The main processing tweaks for yml/xml output formatting are specified
in the default configuration file; if you need to change something, you
can use your own config file in the working directory; note the local
copy must be named ``.ymltoxml.yaml``.  To get a copy of the default
configuration file, do::

  $ cd path/to/work/dir/
  $ ymltoxml --save-config
  $ $EDITOR .ymltoxml.yaml

yagrep
------

A new module is now included for searching keys and values in
YAML files. The ``yagrep`` script also has its own built-in config
file, which can be copied and edited as shown above. In this case the
script is intended to feel more-or-less like ``grep`` so the default
config should Just Work. That said, the script uses the ``dpath``
python library, so you may need to change the default "path" separator
if your data has keys containing forward slashes (see the `upstream
docs`_ for details).

General usage guidelines:

* use the ``-f`` (filter) arg to search for a value string
* follow the (json) output from above to find the key name
* then use the ``-l`` (lookup) arg to extract the values for the key

Useful yagrep config file settings:

:default_separator: change the path separator to something like ``;`` if data
                    has forward slashes
:output_format: set the output format to ``raw`` for unformatted output

::

  $ yagrep -h
  usage: yagrep [-h] [--version] [-v] [-d] [-s] [-f | -l] TEXT FILE [FILE ...]

  Search in YAML files for keys and values.

  positional arguments:
    TEXT               Text string to look for (one-only, required) (default:
                       None)
    FILE               Look in file(s) for text string (at least one, required)
                       (default: None)

  options:
    -h, --help         show this help message and exit
    --version          show program's version number and exit
    -v, --verbose      Display more processing info (default: False)
    -d, --dump-config  Dump default configuration file to stdout (default:
                       False)
    -s, --save-config  save active config to default filename (.yagrep.yml) and
                       exit (default: False)
    -f, --filter       Filter out data not matching input string (no paths)
                       (default: False)
    -l, --lookup       Lookup by key and return list of values for any matches
                       (default: False)


.. _upstream docs: https://github.com/dpath-maintainers/dpath-python

yasort
------

Yet another helper script is included for sorting large (YAML) lists.
The ``yasort`` script also uses its own configuration file, creatively
named ``.yasort.yaml``. The above applies equally to this config file.

::

  $ yasort -h
  usage: yasort [-h] [--version] [-v] [-d] [-s] [FILE ...]

  Sort YAML lists and write new files.

  positional arguments:
    FILE               Process input file(s) to target directory (default: None)

  options:
    -h, --help         show this help message and exit
    --version          show program's version number and exit
    -v, --verbose      Display more processing info (default: False)
    -d, --dump-config  Dump default configuration file to stdout (default:
                       False)
    -s, --save-config  save active config to default filename (.yasort.yml) and
                       exit (default: False)

All of the optional arguments for ``yasort`` are essentially orthogonal to
sorting, thus the only required argument for normal usage is one or more
input files. All of the user settings are in the default configuration file
shown below; use the ``--save-config`` option to create your own config file.

Default yasort.yaml:

.. code-block:: yaml

  ---
  # comments should be preserved
  file_encoding: 'utf-8'
  default_yml_ext: '.yaml'
  output_dirname: 'sorted-out'
  default_parent_key: 'controls'
  default_sort_key: 'rules'
  has_parent_key: true
  preserve_quotes: true
  process_comments: false
  mapping: 4
  sequence: 6
  offset: 4


Features and limitations
------------------------

**NIST control ID munging**

The demo scripts and ``oscal`` module illustrate various forms of control ID
normalization in order to match control IDs from multiple input sources.
Currently, there are 2 primary ID formats, and which one to use is mainly
a user choice:

* AC-01(01)(a) - uppercase with parentheses
* ac-01.01.a - lowercase with dots

Nested controls follow the upstream_ pattern of alternating lettered and
numbered sub-bullets for each level, and the latest rev5 controls add
leading zeros.

The ``xform_id`` function is *idempotent* with the following caveats:

* extraneous whitespace is always dropped
* leading zeros are added to single digit values where needed

.. _upstream: https://github.com/usnistgov/oscal-content

**XML <==> YAML** conversion

We mainly test ymltoxml on mavlink XML message definitions and NIST/SSG
content files, so round-trip conversion *may not* work at all on
arbitrarily complex XML files with namespaces, etc.  The current
round-trip is not exact, due to the following:

* missing encoding is added to version tag
* leading/trailing whitespace in text elements and comments is not preserved
* XML - elements with self-closing tags are converted to full closing tags
* XML - empty elements on more than one line are not preserved

For the files tested (eg, mavlink) the end result is cleaner/shinier XML.

Dev workflows
=============

The following covers two types of workflows, one for tool usage in other
(external) projects, and one for (internal) tool development.

Mavlink use case
----------------

The ymltoxml tools are intended to be part of a larger workflow, ie,
developing custom mavlink message dialects and generating/deploying the
resulting mavlink language interfaces.  To be more specific, for this
example we use a mavlink-compatible component running on a micro-controller,
thus the target language bindings are C and C++.

Tool requirements for the full mavlink workflow:

* initially just recent pymavlink, Python, and Tox_

Both mavlink and pymavlink require a (host) GCC toolchain for full builds,
however, the basic workflow to generate mavlink library headers requires
only Git, Python, and Tox.

.. _mavlink: https://mavlink.io/en/messages/common.html
.. _Tox: https://github.com/tox-dev/tox
.. _XML: https://en.wikipedia.org/wiki/Extensible_Markup_Language
.. _YAML: https://en.wikipedia.org/wiki/YAML

SCAP use case
-------------

The yasort/yagrep tools are also intended to be part of a larger
workflow, mainly working with SCAP content, ie, the scap-security-guide
source files (or just content_). It is currently used to sort profiles
with large numbers of rules, as well as create control files and analyze
existing controls.

The yasort configuration file defaults are based on existing yaml structure,
but feel free to change them for another use case. To adjust how the sorting
works, make a local config file (see above) and edit as needed the following
options:

:output_dirname: directory for output file(s)
:default_parent_key: parent key if sort target is sublist
:default_sort_key: the key you want to sort
:has_parent_key: set true if sorting a sublist
:default_yml_ext: change the output file extension

The rest of the options are for YAML formatting/flow style (see the ruamel_
documentation for formatting details)

.. _content: https://complianceascode.readthedocs.io/en/latest/
.. _ruamel: https://yaml.readthedocs.io/en/latest/

In-repo workflow with Tox
-------------------------

As long as you have git and at least Python 3.8, then the "easy" dev
workflow is to clone this repository and install Tox via your system
package manager, eg::

  $ sudo apt-get update
  $ sudo apt-get install tox


After cloning this repository, you can run the repo checks with the
``tox`` command.  It will build a virtual python environment with
all the dependencies and run the specified commands, eg:

::

  $ git clone https://github.com/sarnold/yaml-tools.git
  $ cd yaml-tools/
  $ tox -e py

The above will run the tests using your (default) system Python;
to specify the Python version and host OS type, run something like::

  $ tox -e py39-linux

To generate a coverage file, run something like the following::

  $ tox -e py,coverage

Additional ``tox`` commands:

* ``tox -e changes`` (re)generate the changelog file
* ``tox -e conv`` round-trip conversion test on mavlink dialect
* ``tox -e dev`` pip "developer" install
* ``tox -e style`` will run flake8 style checks
* ``tox -e lint`` will run pylint (somewhat less permissive than PEP8/flake8 checks)
* ``tox -e mypy`` will run mypy import and type checking
* ``tox -e isort`` will run isort import checks
* ``tox -e clean`` will remove temporary test files

To build/lint the api docs, use the following tox commands:

* ``tox -e docs`` build the documentation using sphinx and the api-doc plugin
* ``tox -e ldocs`` build the docs and run the sphinx link checking
* ``tox -e cdocs`` clean all the generated doc files

Local Tox upgrade
-----------------

Some required Linux environments can be old enough to require "special"
handling (eg, Ubuntu bionic or focal) as shown below. If the Tox_ package
version available via system package manager is less than 4.x, it may be
possible to install the latest Tox version into XDG $HOME directories, eg,
``$HOME/.local/bin``. Note that Ubuntu allows this but Debian frowns on it
so this option may not available.

If the above procedure is supported, try something like the following::

  $ sudo apt-get update
  $ sudo apt-get install python3-venv python3-pip
  $ sudo apt-get purge python3-virtualenv
  $ python3 -m pip install -U pip
  $ source ~/.profile
  $ which pip3
  /home/user/.local/bin/pip3
  $ pip3 install tox
  $ tox --version

Ensure the above version is 4.x and the path displayed starts with
``$HOME/.local``.

Making Changes & Contributing
=============================

We use the gitchangelog_ action to generate our changelog file and GH
Release page, as well as the gitchangelog commit message prefix "tag"
modifiers to help it categorize/filter commits for a tidier changelog.
Please use the appropriate ACTION modifiers in any Pull Requests. Some
examples of commit message summary "tags" are shown in ``.gitchangelog.rc``
file and reproduced below::

  new: usr: support of bazaar implemented
  chg: re-indentend some lines !cosmetic
  new: dev: updated code to be compatible with last version of killer lib.
  fix: pkg: updated year of licence coverage.
  new: test: added a bunch of test around user usability of feature X.
  fix: typo in spelling my name in comment. !minor

See the following docs page (or generate-changelog.rst_ on Github) for more
details.

.. _generate-changelog.rst: https://github.com/sarnold/yaml-tools/blob/main/docs/source/dev/generate-changelog.rst

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

  $ git clone https://github.com/sarnold/yaml-tools
  $ cd yaml-tools/
  $ pre-commit install

It's usually a good idea to update the hooks to the latest version::

    pre-commit autoupdate


SBOM and license info
=====================

This project is now compliant with the REUSE Specification Version 3.3, so the
corresponding license information for all files can be found in the ``REUSE.toml``
configuration file with license text(s) in the ``LICENSES/`` folder.

Related metadata can be (re)generated with the following tools and command
examples.

* reuse-tool_ - REUSE_ compliance linting and sdist (source files) SBOM generation
* sbom4python_ - generate SBOM with full dependency chain

Commands
--------

Use tox to create the environment and run the lint command::

  $ tox -e reuse                      # --or--
  $ tox -e reuse -- spdx > sbom.txt   # generate sdist files sbom

Note you can pass any of the other reuse commands after the ``--`` above.

Use the above environment to generate the full SBOM in text format::

  $ source .tox/reuse/bin/activate
  $ sbom4python --system --use-pip -o <file_name>.txt

Be patient; the last command above may take several minutes. See the
doc links above for more detailed information on the tools and
specifications.

.. _pre-commit: https://pre-commit.com/index.html
.. _reuse-tool: https://github.com/fsfe/reuse-tool
.. _REUSE: https://reuse.software/spec-3.3/
.. _sbom4python: https://github.com/anthonyharrison/sbom4python
.. _gitchangelog: https://github.com/sarnold/gitchangelog


License
=======

This project is licensed under the LGPL license - see the `LICENSE file`_ for
details.

.. _LICENSE file: https://github.com/sarnold/yaml-tools/blob/main/LICENSE


.. |ci| image:: https://github.com/sarnold/yaml-tools/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/sarnold/yaml-tools/actions/workflows/ci.yml
    :alt: CI Status

.. |wheels| image:: https://github.com/sarnold/yaml-tools/actions/workflows/wheels.yml/badge.svg
    :target: https://github.com/sarnold/yaml-tools/actions/workflows/wheels.yml
    :alt: Wheel Status

.. |coverage| image:: https://github.com/sarnold/yaml-tools/actions/workflows/coverage.yml/badge.svg
    :target: https://github.com/sarnold/yaml-tools/actions/workflows/coverage.yml
    :alt: Coverage workflow

.. |badge| image:: https://github.com/sarnold/yaml-tools/actions/workflows/pylint.yml/badge.svg
    :target: https://github.com/sarnold/yaml-tools/actions/workflows/pylint.yml
    :alt: Pylint Status

.. |release| image:: https://github.com/sarnold/yaml-tools/actions/workflows/release.yml/badge.svg
    :target: https://github.com/sarnold/yaml-tools/actions/workflows/release.yml
    :alt: Release Status

.. |cov| image:: https://raw.githubusercontent.com/sarnold/yaml-tools/badges/main/test-coverage.svg
    :target: https://github.com/sarnold/yaml-tools/
    :alt: Test coverage

.. |pylint| image:: https://raw.githubusercontent.com/sarnold/yaml-tools/badges/main/pylint-score.svg
    :target: https://github.com/sarnold/yaml-tools/actions/workflows/pylint.yml
    :alt: Pylint score

.. |reuse| image:: https://api.reuse.software/badge/git.fsfe.org/reuse/api
    :target: https://api.reuse.software/info/git.fsfe.org/reuse/api
    :alt: REUSE status

.. |license| image:: https://img.shields.io/badge/license-LGPL_2.1-blue
    :target: https://github.com/sarnold/yaml-tools/blob/main/LICENSE
    :alt: License (static)

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/yaml-tools?color=blue&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/yaml-tools/releases
    :alt: GitHub tag

.. |python| image:: https://img.shields.io/badge/python-3.8+-blue.svg
    :target: https://www.python.org/downloads/
    :alt: Python

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. |contributors| image:: https://img.shields.io/github/contributors/sarnold/yaml-tools
   :target: https://github.com/sarnold/yaml-tools/
   :alt: Contributors
