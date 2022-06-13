=========================================
 ymltoxml (and xmltoyml) for mavlink xml
=========================================


Developer workflow
==================

Tool requirements:

* initially just recent Python and Tox_

Both mavlink and pymavlink require a (host) GCC toolchain for full builds,
however, the basic workflow to generate the library headers requires only
Git, Python, and Tox.


In-repo workflow with Tox
=========================

As long as you have git and at least Python 3.6, then the "easy" dev
workflow is to clone this repository and install Tox via your system
package manager, eg::

  $ sudo apt-get update
  $ sudo apt-get install tox


.. _Tox: https://github.com/tox-dev/tox
