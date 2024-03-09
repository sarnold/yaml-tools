"""Console script for searching YAML or XML files."""

import argparse
import json
import sys
from pathlib import Path

import dpath
from munch import Munch

from .utils import VERSION as __version__, FileTypeError, load_config
from .ymltoxml import get_input_type

# pylint: disable=R0801


def process_inputs(filepath, text_glob, prog_opts, debug=False):
    """
    Handle file arguments and process them. Return any input data for use
    with ``dpath`` search.

    :param filepath: filename as Path obj
    :param prog_opts: configuration options
    :type prog_opts: dict
    :param debug: enable extra processing info
    :return: data and source type boolean or None
    :handles FileTypeError: if input file is not yaml or xml
    """

    def glob_filter(x):
        """
        Basic search glob to use with dpath.* functions.
        """
        if text_glob in str(x):
            return True
        return False

    fpath = Path(filepath)
    path_sep = prog_opts['default_separator']

    if not fpath.exists():
        print(f'Input file {fpath} not found! Skipping...')
    else:
        if debug:
            print(f'Searching in {fpath}...')

        try:
            _, indata = get_input_type(fpath, prog_opts)
        except FileTypeError as exc:
            print(f'{exc} => {fpath}')
            return None
        if debug:
            print(indata)

        result = dpath.search(indata, '**', afilter=glob_filter, separator=path_sep)
        sys.stdout.write(json.dumps(result, indent=4, sort_keys=True) + '\n')


def main(argv=None):  # pragma: no cover
    """
    Process args and execute search.
    """
    debug = False
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Search in YAML files for keys and values.',
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Display more processing info",
    )
    parser.add_argument(
        '-d',
        '--dump-config',
        action='store_true',
        dest="dump",
        help='Dump default configuration file to stdout',
    )
    parser.add_argument(
        '-s',
        '--save-config',
        action='store_true',
        dest="save",
        help='save active config to default filename (.yagrep.yml) and exit',
    )
    parser.add_argument(
        "-p",
        "--path-keys",
        type=str,
        nargs='+',
        help="Use separate path elements instead of path string",
    )
    parser.add_argument(
        'text',
        nargs='?',
        metavar="TEXT",
        type=str,
        help="Text string to look for",
    )
    parser.add_argument(
        'file',
        nargs='*',
        metavar="FILE",
        type=str,
        help="Look in file(s) for text string",
    )

    args = parser.parse_args()

    cfg, pfile = load_config(yagrep=True)
    popts = Munch.toDict(cfg)

    if args.save:
        cfg_data = pfile.read_bytes()
        def_config = Path('.yagrep.yml')
        def_config.write_bytes(cfg_data)
        sys.exit(0)
    if args.dump:
        sys.stdout.write(pfile.read_text(encoding=popts['file_encoding']))
        sys.exit(0)
    if args.verbose:
        debug = True
    # if not args.file or args.text:
        # parser.print_help()
        # sys.exit(1)

    for filearg in args.file:
        process_inputs(filearg, args.text, popts, debug)


if __name__ == '__main__':
    main()
