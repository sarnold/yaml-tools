#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Transform mavlink-style xml files to/from xml and yaml. Note yaml format uses
custom markup for attributes and comments. See xmltodict docs for details.
"""
import os
import sys
from contextlib import contextmanager
from pathlib import Path

import xmltodict
import yaml as yaml_loader
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from munch import Munch

DEBUG = False


class StrYAML(YAML):
    """
    New API likes dumping straight to file/stdout, so we subclass and
    create 'inefficient' custom string dumper.  <shrug>
    """
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
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


@contextmanager
def open_handle(filename, mode='r', file_encoding='utf-8'):
    """
    Context manager for input data using file or pipe.
    """
    if filename == '-':
        fhandle = sys.stdin.buffer
        fname = fhandle.name
    else:
        # make sure filename str is a Path obj
        filename = Path(filename)
        fhandle = open(filename, mode, encoding=file_encoding)
        fname = filename.name
    try:
        yield (fhandle, fname)
    finally:
        if filename != '-':
            fhandle.close()


def restore_xml_comments(xmls):
    """
    Turn comment elements back into xml comments.
    :param xmls: xml (file) string output from ``unparse``
    :return xmls: processed xml string
    """

    for rep in (("<#comment>", "<!-- "), ("</#comment>", " -->")):
        xmls = xmls.replace(*rep)
    return xmls


def transform_data(payload, direction='to_xml'):
    """
    Produce output data from dict-ish object using ``direction``.
    :param payload: dict: output from xmltodict or yaml loader.
    :param direction: output format, either to_yml or to_xml
    :return: xml
    """
    res = ''
    if 'xml' in direction:
        xml = xmltodict.unparse(payload,
                                short_empty_elements=False,
                                pretty=True,
                                indent='  ')

        res = restore_xml_comments(xml)

    else:
        yaml = StrYAML()
        yaml.indent(mapping=2,
                    sequence=4,
                    offset=2)

        yaml.preserve_quotes = True  # type: ignore
        res = yaml.dump(payload)

    return res


if __name__ == '__main__':
    VERSION = '0.0.0'

    cfg = load_config()

    REDIRECT = '>'
    args = sys.argv[1:]
    if REDIRECT in args:
        redirect_idx = args.index(REDIRECT)
        redirect_args = args[redirect_idx:]
        del args[redirect_idx:]

    if args == ['--version']:
        print(f'[ymltoxml {VERSION}]')
        sys.exit(0)
    if not args:
        args = ['-']
    elif args == ['--verbose']:
        DEBUG = True
    elif args == ['--selftest']:
        print(f'cfg from yaml: {cfg}')
        sys.exit(0)

    # for filearg in args:
    #     with open_handle(filearg) as handle:
    #         if DEBUG:
    #             print("Processing data from {}".format(handle[1]))
    #         process_file(handle[0], handle[1], debug=DEBUG)

    with open_handle('in.yaml') as handle:
        data_in = yaml_loader.load(handle[0], Loader=yaml_loader.Loader)

    data_out = transform_data(data_in)

    with open_handle('out.xml', 'w+') as handle:
        handle[0].write(data_out)
        handle[0].write('\n')
