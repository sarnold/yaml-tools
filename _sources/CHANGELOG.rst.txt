Changelog
=========


0.5.2 (2025-11-30)
------------------

Changes
~~~~~~~
- Restore process_template using string Template from std lib. [Stephen
  L Arnold]

  * update dumper subclass and init template processing with default loader
  * update bandit config due to false positive using the above
  * adjust mypy deps, cleanup some lint and docstrings


0.5.1 (2025-10-24)
------------------

Changes
~~~~~~~
- Extend python workflow matrix to 3.14. [Stephen L Arnold]

  * update changes file for patch release

Fixes
~~~~~
- Remove deprecated option, make score visible in ci, add ignores.
  [Stephen L Arnold]

  * ignore both specific pytest warnings and some very specific pylint
    warnings about open without using with


0.5.0 (2025-05-31)
------------------

New
~~~
- Add reuse config and LICENSES folder, update readme. [Stephen L
  Arnold]
- Start adding type hints, update mypy config. [Stephen Arnold]

Changes
~~~~~~~
- Cleanup type annotations, doc strings, and docs build. [Stephen L
  Arnold]

  * revert to rtd<3 to get version display, update api extensions
  * add small markdown helpers for massaging diagram files in CI
  * remove unused jinja2 bits, update tests and mypy config
- Update config handling, add test for natsort paths. [Stephen L Arnold]

  * cleanup type annotations and importlib resource handling
- Use autoapi extension, cleanup doc bits and dependencies. [Stephen L
  Arnold]
- Use setuptools-scm get_version in gitchangelog.rc, cleanup readme.
  [Stephen L Arnold]

  * install base deps in tox changes env for setuptools-scm import
- Update pre-commit hooks and apply fomrat changes. [Stephen L Arnold]
- Add teuse tox cmd and make toxfile.py reuse compliant. [Stephen L
  Arnold]
- Update versions and permissions ion workflows. [Stephen L Arnold]
- Cleanup on metadata and tox. [Stephen L Arnold]
- Update idchk script to de-duplicate before sorting. [Stephen L Arnold]
- Cleanup doc examples and script output. [Stephen L Arnold]

  * check for zero-length string in input IDs

Fixes
~~~~~
- Cleanup docstrings, let autodoc fill in type info, update readme.
  [Stephen L Arnold]
- Add more type hints until clean, add py.typed marker, adjust tests.
  [Stephen L Arnold]
- Use correct package metadata and cleanup workflows. [Stephen L Arnold]

  * simplify test coverage workflow on py3.12 only

Other
~~~~~
- Create codeql.yml. [Steve Arnold]

  Cleanup default advanced config
- Create dependabot.yml. [Steve Arnold]

  Only for actions so far


0.4.2 (2024-11-03)
------------------

Changes
~~~~~~~
- Signature refactor and test,lint cleanup. [Stephen Arnold]

Fixes
~~~~~
- Cleanup more docstrings and parameter names. [Stephen Arnold]

  * also bump pre-commit deps

Other
~~~~~
- Update changelog for patch release. [Stephen L Arnold]


0.4.1 (2024-08-27)
------------------

New
~~~
- Add config option for jinja2 line statements in template func.
  [Stephen Arnold]

  * cleanup template test data and test func
- Add new_csv_file option, update tests and readme. [Stephen L Arnold]

Changes
~~~~~~~
- Update .gitchangelog.rc and regenerate changelog. [Stephen Arnold]

  * now we can match on more commit messages including dev: tag
- Cleanup jinja template environment, enable block trim. [Stephen
  Arnold]
- Add initial test data and template func, update text reader. [Stephen
  Arnold]

  * make sure text_file_reader handles both ID files and normal text files
- Update tox docs envs and make default separator a semicolon. [Steve
  Arnold]

  * do not forget to use a comma separator for test cfg
- Cleanup readme and docstrings. [Stephen L Arnold]
- Allow for adjustable CSV delimiter in oscal.yaml. [Stephen L Arnold]
- Cleanup unnecessary branches, update expected test output. [Stephen L
  Arnold]
- Refactor for testing, cleanup script imports and test data. [Stephen L
  Arnold]

  * add some new control data files for test support
- Improve xform_id, update tests, cleanup some lint. [Stephen L Arnold]
- Switch oscal text report output to semicolon instead of comma.
  [Stephen L Arnold]
- Add quiet cmdline arg, update attr arg so arg takes precedence.
  [Stephen L Arnold]

  * make sure arg overrides file value, no value means no report
- Remove py38 from test matrix. [Stephen L Arnold]

  * xform_id(id, strip) needs at least py39 if strip is True, so
    fallback to nothing if no member attribute
  * skip strip test on < py39
- Make id-strip default off, update pre-commit cfg, add cleanup.
  [Stephen L Arnold]
- Allow xform_id to strip trailing zeros from ID strings. [Stephen L
  Arnold]

Fixes
~~~~~
- Cleanup test data for new args and output. [Stephen L Arnold]


0.4.0 (2024-05-16)
------------------

New
~~~
- Move nist profile ids from tests to pkg data, update srcs/tests.
  [Steve Arnold]

  * move profile ID text files to package data
  * add some helper funcs for profile ID handling
  * add related test code to test_misc
  * minor refactoring in templates and text_data_writer
  * cleanup tests and test data
- Add ID set analysis to oscal module, update tests and default cfg.
  [Steve Arnold]
- Add set subclass based on list, with ordering and sort. [Steve Arnold]

  * add tests and cleanup code
- Give oscal module its own config, refactor load_config and tests.
  [Steve Arnold]

  * refactor modules for updated load_config args !minor
  * migrate appropriate config settings to new oscal
- Add analysis script using SSG nist control files. [Steve Arnold]

  * update project files for new dependencies
- Add templates module with tests, update project files. [Steve Arnold]

  * note this is still WIP (with bugs even)
- Add output formatter func with tests, add support for pystache. [Steve
  Arnold]

  * pystache is currently a simple render func for template-y yaml
- Add file reader to handle csv, json, yaml, and simple text files.
  [Steve Arnold]

  * for each type, parse into a list of objects and return the list
  * where simple text files are something like the control IDs
    in tests/data
- Test fuzzy-match for analyze script, consolidate code. [Steve Arnold]

  * limit fuzzy match results using startswith input ID string
  * cleanup package modules and tests, move initial profile funcs
- Add stub module for oscal data, update packaging and tox files. [Steve
  Arnold]

  * add .repolite.yml for syncing oscal-content repo
  * update tests and vendor tox plugin for shared envs

Changes
~~~~~~~
- Restore missing py version and update package name. [Steve Arnold]

  * fixes ci release workflow
- Add more control status reporting, update oscal yaml config. [Steve
  Arnold]
- Cleanup deps and docstrings, add set compare to demo script. [Steve
  Arnold]
- Still more readme cleanup. [Steve Arnold]
- Move main module and rename leftover refs, cleanup some lint. [Steve
  Arnold]
- Commit initail name changes; package, imports, readme. [Steve Arnold]
- Make new_csv_hdrs a list again, add ID column. [Steve Arnold]

  * allow substring match in between exact match and none
  * save chk script and update default oscal.yaml
- Oscal module and test cleanup, update packaging. [Steve Arnold]

  * add sorted output option for ssg control set match
  * eliminate unnecessary variable in yasort module
  * update test data and move most output to verbose only
  * update project files with natsort package dep
- Wire up alternate content and use-ssg arg, update tests. [Steve
  Arnold]

  * update default config keys for oscal module
- Add csv output format, flesh out oscal, cleanup code/tests. [Steve
  Arnold]

  * make sure text data read/write supports the same formats
  * add simple consumer test script for the above
- Make sure yagrep uses new output func, cleanup readme. [Steve Arnold]
- Bump tox workflow deps and cleanup/improve readme. [Steve Arnold]
- Bump all workflow action versions. [Steve Arnold]
- Add another text_file_reader consumer and cleanup some lint. [Steve
  Arnold]
- Flesh out argparse and yaml config keys. [Steve Arnold]

Fixes
~~~~~
- Make sure ID lookup works for both content sources. [Steve Arnold]

  * account for differences in SSG vs NIST control formats, at least
    enough for the basic ID set matching
  * oscal default glob should limit the search to either resolved profiles
    only or use the catalog sources
- Cleanup pylint cruft and update test data. [Steve Arnold]

  * also apply pre-commit formatting fixes
- Add missing test and import, update tox file. [Steve Arnold]
- Only transform input IDs if lower, add full OE expanded list. [Steve
  Arnold]
- Account for longer ID strings, update changelog and repolite cfgs.
  [Steve Arnold]

  * update tests and older analysis script
  * bump requirements-sync.txt for new repolite release
- Add more depth to string xform and tests. [Steve Arnold]

  * update line length in pep8speaks config
- Cleanup docstrings after sphinx checks. [Steve Arnold]

Other
~~~~~
- Pre-release cleanup, update changelog and fix readme typos. [Steve
  Arnold]
- Dev: add csv file munge option, cleanup oscal files. [Steve Arnold]

  * add munge file arg to pass in csv data to compare and append
    a column for id set status, eg, whether ids in the input list
    are present in the csv data, and then mark the new column Y/N
  * short-circuit munge file arg and feed it single column of
    control IDs
- Add small set of test IDs from openembedded profile. [Steve Arnold]


0.3.0 (2024-03-12)
------------------

New
~~~
- Add new console script, update reqs and packaging. [Steve Arnold]
- Add support for simple control ID analysis. [Steve Arnold]

  * add utility functions for file handling and profile from filename
  * update misc tests, add small-ish test data file with IDs
  * add a first-cut script to test input IDs against oscal profile IDs

Changes
~~~~~~~
- Add dev workflow dependency and update clean args. [Steve Arnold]
- Cleanup new feature bits and update documentation. [Steve Arnold]

  * use dpath.values for initial path search, and either dpath or
    nested_lookup for extracting values
  * update readme for new script, update all the usage bits
  * add new tests and update existing tests
  * expand and cleanup tox file
- Add new feature tests, update existing tests. [Steve Arnold]
- Move input data sort to output var, update tox file. [Steve Arnold]
- Cleanup script, func, docstrings, update tests. [Steve Arnold]

Fixes
~~~~~
- Re-order yasort arg handling, update analyze script. [Steve Arnold]
- Remove py37 from workflow matrix, fix test on windows. [Steve Arnold]
- Cleanup some lint. [Steve Arnold]


0.2.2 (2023-09-05)
------------------

New
~~~
- Add a changelog file and gitchangelog cfg, add to docs build. [Stephen
  L Arnold]
- Add coverage workflow and update readme. [Stephen L Arnold]
- Add test fixtures annd more tests, cleanup tox and test cfg. [Stephen
  L Arnold]

Changes
~~~~~~~
- Bump changelog for release, add tox cmd to (re)generate changes.
  [Stephen L Arnold]
- Cleanup docstrings and readme usage. [Stephen L Arnold]
- Still more readme cleanup. [Stephen L Arnold]
- Organnize the one test, cleanup test cfg, start using pytest. [Stephen
  L Arnold]
- Post-fix cleanup and simplify list sorts. [Stephen L Arnold]
- Minor refactoring of sorts, save current check state. [Stephen L
  Arnold]
- Refactor with importlib and setuptools-scm. [Stephen L Arnold]

  * sorting is still an issue and apparently very !wip
- Refactor from optparse to argparse, cleanup docs/docstrings. [Stephen
  L Arnold]

Fixes
~~~~~
- Clean up docstrings in utils. [Stephen L Arnold]
- Use sort method instead of sorted() to preserve comments. [S.
  Lockwood-Childs]

  sorted() returs a normal list which loses info in extra members
  of the CommentedSeq object, but the sort method sorts elements
  inside the existing CommentedSeq object
- Bump importlib-resources version for CI compatibility. [Stephen L
  Arnold]

  * sprinkle some pylint: disable for issues that are not issues


0.2.1 (2023-07-16)
------------------

New
~~~
- Wire up sorting opts, cleanup config file, update readme. [Stephen L
  Arnold]

  * add sdist artifact to release workflow

Fixes
~~~~~
- Ci: update artifact conditional. add inspection step. [Stephen L
  Arnold]


0.2.0 (2023-07-15)
------------------

New
~~~
- Add sorting script and default config, cleanup lint. [Stephen L
  Arnold]
- Add more project docs to sphinx build. [Stephen L Arnold]

  * filter out/remove local file links for docs build
- Add more config options, update tool deps and readme. [Stephen L
  Arnold]

  * allow more user-facing config options, add munch-stubs for mypy
  * update tool deps and cfgs to use new type stubs
  * update readme usage description

Changes
~~~~~~~
- Readme cleanup, add note about yasort script. [Stephen L Arnold]
- Dbg: run tox bare-ass in github runner for workflow debug. [Stephen L
  Arnold]
- Import cleanup, add tox dev cmd, update workflows. [Stephen L Arnold]
- Update readme with new usage output. [Stephen L Arnold]

Fixes
~~~~~
- Cleanup GH action deprecation warnings in all workflows. [Stephen L
  Arnold]
- Add pylint pre-cmd for version, revert debug changes. [Stephen L
  Arnold]
- Loop through parent key, cleanup spurious warning and typo. [Stephen L
  Arnold]
- Use new path to source rst for github readme rendering. [Stephen L
  Arnold]
- Replace sys.argv with option parser, wire up options and args.
  [Stephen L Arnold]

  * yes, optparse is deprected so may be replaced in the future

Other
~~~~~
- Adjust importlib version cutoff in reqs. [Stephen L Arnold]
- Move some shared code to separate module, update pre-commit cfg.
  [Stephen L Arnold]


0.1.0 (2022-06-22)
------------------

New
~~~
- Add pre-commit and pep8speaks configs, apply some cleanup. [Stephen L
  Arnold]
- Add sphinx api-doc build, update readme and doc strings. [Stephen L
  Arnold]
- Add arg to dump default config yaml to stdout. [Stephen L Arnold]

Changes
~~~~~~~
- Update readme and usage output. [Stephen L Arnold]
- Flatten cfg file, use single cfg object, cleanup doc strings. [Stephen
  L Arnold]
- Integrate version, add packaging files, flesh out cfg options.
  [Stephen L Arnold]
- Install pymavlink using pip without mavnative, rename MDEF var.
  [Stephen L Arnold]
- Refactor input handling, update tox and readme files. [Stephen L
  Arnold]
- Flesh out package layout, update readme/project files. [Stephen L
  Arnold]

  * main module/script currently one direction only
  * update tox file for path changes
  * generate munch type stubs, apply isort fixes

Fixes
~~~~~
- Replace old thing/new thing => use importlib for cfg file. [Stephen L
  Arnold]

  * use external importlib pkgs first
  * make mypy ignore one of the 2 importlib imports
  * install pkg for command-line test
- Flesh out gh OS matrix. [Stephen L Arnold]

Other
~~~~~
- Add docs workflow, fix broken doc link, update ci workflow. [Stephen L
  Arnold]
- Cleanup metadata/packaging and workflow files. [Stephen L Arnold]
- Add more CI workflows for wheels, pylint, release. [Stephen L Arnold]


0.0.0 (2022-06-19)
------------------

Changes
~~~~~~~
- Add simple ci workflow, update tox file with gh-actions. [Stephen L
  Arnold]
- Apply isort fixes. [Stephen L Arnold]
- Add tool configs, update readme and tox files. [Stephen L Arnold]
- Add requirements file and mypy config, update tox file. [Stephen L
  Arnold]

Fixes
~~~~~
- Cleanup unused code/imports, add one type ignore for mypy. [Stephen L
  Arnold]

  * upstream ruamel.yaml preserve_quotes = True type error
- Use paparazzi.xml from pymavlink for test input. [Stephen L Arnold]

Other
~~~~~
- Initial commit with test scripts and tox driver. [Stephen L Arnold]
- Initial commit. [Steve Arnold]
