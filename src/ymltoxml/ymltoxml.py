#!/usr/bin/env python

# Copyright 2022 Stephen L Arnold
#
# This is free software, licensed under the LGPL-2.1 license
# available in the accompanying LICENSE file.

"""
Transform YAML to XML and XML to YAML.
"""

import os
import sys
from pathlib import Path

try:
    from importlib_metadata import version
except ImportError:
    from importlib.metadata import version
try:
    from importlib_resources import files
except ImportError:
    from importlib.resources import files  # type: ignore

import xmltodict
import yaml as yaml_loader
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from munch import Munch


class FileTypeError(Exception):
    """Raise when the file extension is not '.xml', '.yml', or '.yaml'"""
    __module__ = Exception.__module__


class StrYAML(YAML):
    """
    New API likes dumping straight to file/stdout, so we subclass and
    create 'inefficient' custom string dumper.  <shrug>
    """
    def dump(self, data, stream=None, **kw):
        stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        return stream.getvalue()


def load_config(file_encoding='utf-8'):
    """
    Load yaml configuration file and munchify the data. If local file is
    not found in current directory, the default will be loaded.
    :param str file_encoding: cfg file encoding
    :return tuple: Munch cfg obj and cfg file as Path obj
    """
    cfgfile = Path('.ymltoxml.yaml')
    if not cfgfile.exists():
        cfgfile = files('ymltoxml.data').joinpath('ymltoxml.yaml')
    cfgobj = Munch.fromYAML(cfgfile.read_text(encoding=file_encoding))

    return cfgobj, cfgfile


def get_input_type(filepath, prog_opts):
    """
    Check filename extension, open and process by file type, return type
    flag and data from appropriate loader.
    :param Path filepath: filename as Path obj
    :return tuple: destination type flag and file data
    """
    to_xml = False
    data_in = None

    if filepath.name.lower().endswith(('.yml', '.yaml')):
        with filepath.open() as infile:
            data_in = yaml_loader.load(infile, Loader=yaml_loader.Loader)
        to_xml = True
    elif filepath.name.lower().endswith('.xml'):
        with filepath.open('r+b') as infile:
            data_in = xmltodict.parse(infile,
                                      process_comments=prog_opts['process_comments'])
    else:
        raise FileTypeError("FileTypeError: unknown input file extension")
    return to_xml, data_in


def restore_xml_comments(xmls):
    """
    Turn tagged comment elements back into xml comments.
    :param str xmls: xml (file) output from ``unparse``
    :return str xmls: processed xml string
    """
    for rep in (("<#comment>", "<!-- "), ("</#comment>", " -->")):
        xmls = xmls.replace(*rep)
    return xmls


def transform_data(payload, prog_opts, to_xml=True):
    """
    Produce output data from dict-ish object using ``direction``.
    :param payload: input from xmltodict or yaml loader.
    :param dict prog_opts: configuration options
    :param bool to_xml: output direction, ie, if to_xml is True then output
                        data is XML format.
    :return str res: output file data in specified format.
    """
    res = ''
    if to_xml:
        xml = xmltodict.unparse(payload,
                                short_empty_elements=prog_opts['short_empty_elements'],
                                pretty=prog_opts['pretty'],
                                indent=prog_opts['indent'])

        if prog_opts['process_comments']:
            res = restore_xml_comments(xml)

    else:
        yaml = StrYAML()
        yaml.indent(mapping=prog_opts['mapping'],
                    sequence=prog_opts['sequence'],
                    offset=prog_opts['offset'])

        yaml.preserve_quotes = True  # type: ignore
        res = yaml.dump(payload)

    return res


def main(argv=None):
    """
    Transform mavlink-style xml files to/from xml and yaml. Note yaml format uses
    custom markup for attributes and comments. See xmltodict docs for details.
    """

    debug = False

    if os.getenv('VERBOSE') and os.getenv('VERBOSE') == '1':
        debug = True

    cfg, pfile = load_config()
    popts = Munch.toDict(cfg)

    if argv is None:
        argv = sys.argv
    args = argv[1:]

    if args == ['--version']:
        print(f'[ymltoxml {VERSION}]')
        sys.exit(0)
    elif args == ['--dump-config']:
        sys.stdout.write(pfile.read_text(encoding=popts['file_encoding']))
        sys.exit(0)

    for filearg in args:
        fpath = Path(filearg)
        if not fpath.exists():
            print(f'Input file {fpath} not found! Skipping...')
        else:
            if debug:
                print(f'Processing data from {filearg}')

            try:
                from_yml, indata = get_input_type(fpath, popts)
            except FileTypeError as exc:
                print(f'{exc} => {fpath}')
                break

            outdata = transform_data(indata, popts, to_xml=from_yml)

            if from_yml:
                fpath.with_suffix('.xml').write_text(outdata + '\n',
                                                     encoding=popts['file_encoding'])
            else:
                fpath.with_suffix('.yaml').write_text(outdata,
                                                      encoding=popts['file_encoding'])


VERSION = version("ymltoxml")


if __name__ == '__main__':
    main()
