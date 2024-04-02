"""
The main init, run, and self-test functions for oscal extract.
"""

import argparse
import importlib
import sys
from collections import deque
from pathlib import Path

from munch import Munch
from nested_lookup import nested_lookup

from .templates import xform_id
from .utils import (
    VERSION,
    FileTypeError,
    get_filelist,
    load_config,
    text_file_reader,
)

# pylint: disable=R0801


def load_input_data(filepath, prog_opts, debug=False):
    """
    Find and gather the inputs, ie, content file(s) and user control IDs,
    into a tuple of lists (id_list, file_tuple_list). Load up the queues
    and return a tuple of both queues and the list of normalized user IDs
    from ``filepath``.
    """
    id_queue = deque()
    ctl_queue = deque()
    file_tuples = []
    in_list = Path(filepath).read_text(encoding=prog_opts['file_encoding']).splitlines()

    in_ids = [xform_id(x) for x in in_list] if in_list[0].islower() else in_list
    if debug:
        print(f'Normalized input Ids: {in_ids}')

    ctl_files = get_filelist(
        prog_opts['default_ssg_path'],
        prog_opts['default_ssg_glob'],
        debug,
    )

    for file in ctl_files:
        file_tuples.append((file, Path(file).name))
    if debug:
        print(f'Using control file(s): {file_tuples}')

    for path in file_tuples:
        print(f'Extracting IDs from {path[1]}')

        try:
            indata = text_file_reader(Path(path[0]), prog_opts)
        except FileTypeError as exc:
            print(f'{exc} => {Path(path[0])}')

        id_queue.append(
            (path[1], [x for x in nested_lookup('id', indata) if x.isupper()])
        )

        for ctl_id in nested_lookup(prog_opts['default_lookup_key'], indata)[0]:
            ctl_queue.append((ctl_id['id'], ctl_id))

    if debug:
        print(f'ID queue Front: {id_queue[0]}')
        print(f'Control queue Front: {ctl_queue[0]}')
        print(f"\nUser control Ids -> {len(in_ids)}")

    return in_ids, id_queue, ctl_queue


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
        print(f'Checking if {opts.default_content_path} exists')
        try:
            ret = Path(opts.default_content_path).resolve(strict=True)
            print(f'  Resolved: {ret}')
        except (FileNotFoundError, RuntimeError) as exc:
            print(f"  {repr(exc)}")
    except (AttributeError, KeyError) as exc:
        print("Config is missing key 'default_content_path'! ")
        print(f"  {repr(exc)}")

    print("-" * 80)


def main(argv=None):  # pragma: no cover
    """
    Collect and process command options/arguments and then process data.
    """
    if argv is None:
        argv = sys.argv

    ucfg, pfile = load_config(Path(__file__).stem)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Extract data from OSCAL or SSG content sources',
    )
    parser.add_argument('--version', action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument(
        '-t', '--test', help='run sanity checks and exit', action='store_true'
    )
    parser.add_argument(
        '-u', '--use-ssg', help='use ssg content sources', action='store_true'
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="display more processing info",
    )
    parser.add_argument(
        '-d',
        '--dump-config',
        help="dump active configuration to stdout and exit",
        action='store_true',
        dest="dump",
    )
    parser.add_argument(
        '-s',
        '--save-config',
        action='store_true',
        dest="save",
        help='save active config to default filename (.oscal.yml) and exit',
    )
    parser.add_argument(
        'file',
        nargs='?',
        metavar="FILE",
        type=str,
        help="path to input file with control IDs",
    )

    args = parser.parse_args()

    if args.save:
        cfg_data = pfile.read_bytes()
        Path(f'.oscal{ucfg.default_ext}').write_bytes(cfg_data)
        sys.exit(0)
    if args.dump:
        sys.stdout.write(Munch.toYAML(ucfg))
        sys.exit(0)
    if args.test:
        self_test(ucfg)
        sys.exit(0)
    if not args.file:
        parser.print_usage()
        print("oscal: error: the following arguments are required: FILE")
        sys.exit(1)
    infile = args.file
    if not Path(infile).exists():
        print(f'Input file {infile} not found!')
        sys.exit(1)

    if args.verbose:
        print(f"Using path to content: {ucfg.default_content_path}")
        print(f"Using input file: {infile}")

    inids, ids, ctls = load_input_data(infile, args, args.verbose)


if __name__ == "__main__":
    main()  # pragma: no cover
