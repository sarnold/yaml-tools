#!/usr/bin/env python

# Copyright 2022 Stephen L Arnold
#
# This is free software, licensed under the LGPL-2.1 license
# available in the accompanying LICENSE file.

"""
Converts YAML to XML and XML to YAML.
"""

import os
import sys
from pathlib import Path

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

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
    :return: Munch cfg obj
    """
    cfgfile = Path('.ymltoxml.yaml')
    if not cfgfile.exists():
        pkg_path = os.path.dirname(sys.modules['ymltoxml'])
        cfgfile = Path(os.path.join(pkg_path, 'data', 'ymltoxml.yaml'))

    return Munch.fromYAML(cfgfile.read_text(encoding=file_encoding))


def get_input_type(filepath, prog_opts):
    """
    Check filename extension, open and process by file type, return type
    flag and data from appropriate loader.
    :param filepath: filename as Path obj
    :return: tuple with file data and destination type flag
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
    Turn comment elements back into xml comments.
    :param xmls: xml (file) string output from ``unparse``
    :return xmls: processed xml string
    """
    for rep in (("<#comment>", "<!-- "), ("</#comment>", " -->")):
        xmls = xmls.replace(*rep)
    return xmls


def transform_data(payload, yml_opts, xml_opts, to_xml=True):
    """
    Produce output data from dict-ish object using ``direction``.
    :param payload: input from xmltodict or yaml loader.
    :param to_xml: output direction, ie, if to_xml is True then output
                   data is XML format.
    :return result: output file (str) in specified format.
    """
    res = ''
    if to_xml:
        xml = xmltodict.unparse(payload,
                                short_empty_elements=xml_opts['short_empty_elements'],
                                pretty=xml_opts['pretty'],
                                indent=xml_opts['indent'])

        res = restore_xml_comments(xml)

    else:
        yaml = StrYAML()
        yaml.indent(mapping=yml_opts['mapping'],
                    sequence=yml_opts['sequence'],
                    offset=yml_opts['offset'])

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

    cfg = load_config()
    popts = Munch.toDict(cfg.prog_opts[0])
    yopts = Munch.toDict(cfg.yml_opts[0])
    xopts = Munch.toDict(cfg.xml_opts[0])

    if argv is None:
        argv = sys.argv
    args = argv[1:]

    if args == ['--version']:
        print(f'[ymltoxml {VERSION}]')
        sys.exit(0)
    elif args == ['--selftest']:
        print('cfg items from yaml:')
        print(f'  {cfg}')
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

            outdata = transform_data(indata, yopts, xopts, to_xml=from_yml)

            if from_yml:
                fpath.with_suffix('.xml').write_text(outdata + '\n',
                                                     encoding=popts['file_encoding'])
            else:
                fpath.with_suffix('.yaml').write_text(outdata,
                                                      encoding=popts['file_encoding'])


VERSION = version("ymltoxml")


if __name__ == '__main__':
    main()
