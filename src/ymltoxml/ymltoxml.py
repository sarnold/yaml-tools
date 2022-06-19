#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Transform mavlink-style xml files to/from xml and yaml. Note yaml format uses
custom markup for attributes and comments. See xmltodict docs for details.
"""
import os
import sys
from pathlib import Path

import xmltodict
import yaml as yaml_loader
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

from munch import Munch


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


def get_input_type(filepath):
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
            data_in = xmltodict.parse(infile, process_comments=True)

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


def transform_data(payload, to_xml=True):
    """
    Produce output data from dict-ish object using ``direction``.
    :param payload: dict: output from xmltodict or yaml loader.
    :param to_xml: output format, ie, XML if to_xml is True
    :return result: output data in to_format
    """
    res = ''
    if to_xml:
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
    DEBUG = False

    if os.getenv('VERBOSE') and os.getenv('VERBOSE') == '1':
        DEBUG = True

    cfg = load_config()

    args = sys.argv[1:]

    if args == ['--version']:
        print(f'[ymltoxml {VERSION}]')
        sys.exit(0)
    elif args == ['--selftest']:
        print(f'cfg from yaml: {cfg}')
        sys.exit(0)

    for filearg in args:
        fpath = Path(filearg)
        if not fpath.exists():
            print(f'Input file {fpath} not found! Skipping...')
        else:
            if DEBUG:
                print(f'Processing data from {filearg}')
            from_yml, indata = get_input_type(fpath)
            outdata = transform_data(indata, to_xml=from_yml)
            if from_yml:
                fpath.with_suffix('.xml').write_text(outdata + '\n', encoding='utf-8')
            else:
                fpath.with_suffix('.yaml').write_text(outdata, encoding='utf-8')
