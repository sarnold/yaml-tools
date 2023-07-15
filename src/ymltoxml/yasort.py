# -*- coding: utf-8 -*-
"""Console script for sorting YAML lists."""

import sys
from optparse import OptionParser  # pylint: disable=W0402
from pathlib import Path

from munch import Munch

from ._version import __version__
from .utils import FileTypeError, StrYAML, load_config

# pylint: disable=R0801

def get_input_yaml(filepath, prog_opts):
    """
    Check filename extension, open and munchify contents, return data.

    :param filepath: filename as Path obj
    :param prog_opts: configuration options
    :type prog_opts: dict
    :return data_in: file data
    :raises FileTypeError: if the input file is not yaml
    """
    data_in = None

    if filepath.name.lower().endswith(('.yml', '.yaml')):
        data_in = Munch.fromYAML(filepath.read_text(encoding=prog_opts['file_encoding']))
    else:
        raise FileTypeError("FileTypeError: unknown input file extension")
    return data_in


def sort_list_data(payload, prog_opts):
    """
    Produce output data from dict-ish object.

    :param payload: Munch obj representing YAML input data
    :param prog_opts: configuration options
    :type prog_opts: dict
    :return res: yaml dump of sorted input
    """
    res = ''
    yaml = StrYAML()
    yaml.indent(
        mapping=prog_opts['mapping'],
        sequence=prog_opts['sequence'],
        offset=prog_opts['offset'],
    )
    yaml.preserve_quotes = prog_opts['preserve_quotes']

    # this assumes specific openscap content structure
    for idx in range(len(payload.controls)):
        payload['controls'][idx]['rules'] = sorted(payload['controls'][idx]['rules'])
    res = yaml.dump(Munch.toDict(payload))

    return res


def process_inputs(filepath, prog_opts, debug=False):
    """
    Handle file arguments and process them. Write new (sorted) files to
    the 'sorted-out/' directory in the current working directory.

    :param filepath: filename as Path obj
    :param prog_opts: configuration options
    :type prog_opts: dict
    :param debug: enable extra processing info
    :return None:
    :handles FileTypeError: if input file is not yml
    """
    fpath = Path(filepath)
    outdir = Path(prog_opts['output_dirname'])
    opath = outdir.joinpath(fpath.stem)

    if not fpath.exists():
        print(f'Input file {fpath} not found! Skipping...')
    else:
        if debug:
            print(f'Processing data from {fpath}')

        try:
            indata = get_input_yaml(fpath, prog_opts)
        except FileTypeError as exc:
            print(f'{exc} => {fpath}')
            return

        outdata = sort_list_data(indata, prog_opts)

        new_opath = opath.with_suffix(prog_opts['default_yml_ext'])
        if debug:
            print(f'Writing processed data to {new_opath}')
        new_opath.write_text(outdata, encoding=prog_opts['file_encoding'])


def main(argv=None):
    """
    Transform YAML to XML and XML to YAML.
    """
    debug = False
    cfg, pfile = load_config(yasort=True)
    popts = Munch.toDict(cfg)

    if argv is None:
        argv = sys.argv
    parser = OptionParser(
        usage="usage: %prog [options] arg1 arg2", version=f"%prog {__version__}"
    )
    parser.description = 'Sort YAML lists and write new files.'
    parser.add_option(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="Display more processing info",
    )
    parser.add_option(
        '-d',
        '--dump-config',
        action='store_true',
        dest="dump",
        help='Dump default configuration file to stdout',
    )

    (options, args) = parser.parse_args()

    if options.verbose:
        debug = True
    if options.dump:
        sys.stdout.write(pfile.read_text(encoding=popts['file_encoding']))
        sys.exit(0)
    if len(args) > 0:
        output_dir = Path(popts['output_dirname'])
        if debug:
            print(f'Creating output directory {output_dir}')
        output_dir.mkdir(exist_ok=True)
        for filearg in args:
            process_inputs(filearg, popts, debug=debug)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
