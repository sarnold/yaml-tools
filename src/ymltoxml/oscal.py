"""
The main init, run, and self-test functions for oscal extract.
"""

import argparse
import importlib
import sys
from pathlib import Path

from munch import Munch

from .utils import VERSION, load_config


def self_test(opts):
    """
    Basic sanity check using ``import_module``.
    """
    print("Python version:", sys.version)
    print("-" * 80)

    modlist = ['ymltoxml.__init__', 'ymltoxml.oscal', 'ymltoxml.utils']
    for modname in modlist:
        try:
            print(f'Checking module {modname}')
            mod = importlib.import_module(modname)
            print(mod.__doc__)

        except (NameError, KeyError, ModuleNotFoundError) as exc:
            print("FAILED: %s", repr(exc))

    try:
        print(f'Checking if {opts.default_oscal_dir} exists')
        try:
            ret = Path(opts.default_oscal_dir).resolve(strict=True)
            print(f'  Resolved: {ret}')
        except (FileNotFoundError, RuntimeError) as exc:
            print(f"  {repr(exc)}")
    except (AttributeError, KeyError) as exc:
        print("Config is missing key 'default_oscal_dir'! ")
        print(f"  {repr(exc)}")

    print("-" * 80)


def main(argv=None):  # pragma: no cover
    """
    Collect and process command options/arguments and then process data.
    """
    if argv is None:
        argv = sys.argv

    ucfg, _ = load_config(yagrep=True)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Extract data from OSCAL content repo',
    )
    parser.add_argument('--version', action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument('-t', '--test', help='Run sanity checks', action='store_true')
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display more processing info",
    )
    parser.add_argument(
        '-d',
        '--dump-config',
        help="dump active configuration to stdout",
        action='store_true',
        dest="dump",
    )

    args = parser.parse_args()

    if args.dump:
        sys.stdout.write(Munch.toYAML(ucfg))
        sys.exit(0)
    if args.test:
        self_test(ucfg)
        sys.exit(0)


if __name__ == "__main__":
    main()  # pragma: no cover
