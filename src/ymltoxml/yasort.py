# -*- coding: utf-8 -*-
"""Console script for sorting YAML lists."""

import re
import sys
from optparse import OptionParser  # pylint: disable=W0402
from pathlib import Path

from munch import Munch
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq

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

    def replace_curlys(data):
        """
        Replace original outside curly brace with angle bracket.
        """
        data = re.sub(r'\s{{{\s', ' <{{ ', data)
        return re.sub(r'\}}}\s', '}}> ', data)

    data_in = None
    yaml = YAML()

    if filepath.name.lower().endswith(('.yml', '.yaml')):
        with open(filepath, encoding=prog_opts['file_encoding']) as fp:
            file_data = fp.read()
        munged_data = replace_curlys(str(file_data))
        data_in = yaml.load(munged_data)
    else:
        raise FileTypeError("FileTypeError: unknown input file extension")
    return data_in


def sort_list_data(payload, prog_opts):
    """
    Set YAML formatting and sort keys from config, produce output data
    from input dict-ish object.

    :param payload: Munch obj representing YAML input data
    :param prog_opts: configuration options
    :type prog_opts: dict
    :return res: yaml dump of sorted input
    """
    res = ''

    # this should work for list/sublist structure
    sublist = prog_opts['has_parent_key']
    pkey_name = prog_opts['default_parent_key']
    skey_name = prog_opts['default_sort_key']

    if sublist:  # sort one or more sublists
        if prog_opts['process_comments']:
            for idx in range(len(payload[pkey_name])):
                root_comment = payload.ca
                payload = CommentedSeq(
                    sorted(payload, key=lambda x: x[pkey_name][idx][skey_name])
                )
                payload._yaml_comment = root_comment
        else:
            for idx in range(len(payload[pkey_name])):
                payload[pkey_name][idx][skey_name] = sorted(
                    payload[pkey_name][idx][skey_name]
                )
    else:  # one top-level list
        if prog_opts['process_comments']:
            root_comment = payload.ca
            # payload[skey_name] = sorted(payload[skey_name])
            payload = CommentedSeq(sorted(payload, key=lambda x: x[skey_name]))
            payload._yaml_comment = root_comment
        else:
            payload[skey_name] = sorted(payload[skey_name])

    yamld = StrYAML()
    yamld.indent(
        mapping=prog_opts['mapping'],
        sequence=prog_opts['sequence'],
        offset=prog_opts['offset'],
    )
    yamld.preserve_quotes = prog_opts['preserve_quotes']

    res = yamld.dump(payload)

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

    def replace_angles(data):
        """
        Replace left angle bracket and restore original curly brace.
        """
        data = re.sub(r'\s<{{\s', ' {{{ ', data)
        return re.sub(r'\}}>\s', '}}} ', data)

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

        restored_data = replace_angles(outdata)

        new_opath = opath.with_suffix(prog_opts['default_yml_ext'])
        if debug:
            print(f'Writing processed data to {new_opath}')
        new_opath.write_text(restored_data, encoding=prog_opts['file_encoding'])


def main(argv=None):
    """
    Read/write SSG YAML files with sorted rules.
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
