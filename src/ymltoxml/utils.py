"""
Shared utility code.
"""

import csv
import json
import re
import sys
from pathlib import Path

import yaml as yaml_loader
from munch import Munch
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version

if sys.version_info < (3, 10):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

EXTENSIONS = ['.csv', '.json', '.txt', '.yaml', '.yml']
VERSION = version('ymltoxml')


class FileTypeError(Exception):
    """
    Raise when the file extension is not '.xml', '.yml', or '.yaml'.
    """

    __module__ = Exception.__module__


class StrYAML(YAML):
    """
    New API likes dumping straight to file/stdout, so we subclass and
    create 'inefficient' custom string dumper.
    """

    def dump(self, data, stream=None, **kw):
        stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        return stream.getvalue()


def get_filelist(dirpath, filepattern='*.txt', debug=False):
    """
    Get path objects matching ``filepattern`` starting at ``dirpath`` and
    return a list of matching paths for any files found.

    :param dirpath: directory name to start file search
    :param filepattern: str of the form ``*.<ext>``
    :param debug: increase output verbosity
    :return: list of path strings
    """
    file_list = []
    filenames = Path(dirpath).rglob(filepattern)
    for pfile in list(filenames):
        file_list.append(str(pfile))
    if debug:
        print(f'Found file list: {file_list}')
    return file_list


def load_config(file_encoding='utf-8', yasort=False, yagrep=False, debug=False):
    """
    Load yaml configuration file and munchify the data. If local file is
    not found in current directory, the default will be loaded.

    :param file_encoding: file encoding of config file
    :param yasort: True for yasort config
    :param debug: enable extra processing info
    :type file_encoding: str
    :type yasort: bool
    :return: Munch cfg obj and cfg file as Path obj
    :rtype: tuple
    """
    prog_name = 'ymltoxml'
    if yasort:
        prog_name = 'yasort'
    if yagrep:
        prog_name = 'yagrep'
    defconfig = Path(f'.{prog_name}.yml')

    cfgfile = defconfig if defconfig.exists() else Path(f'.{prog_name}.yaml')
    if not cfgfile.exists():
        cfgfile = importlib_resources.files('ymltoxml.data').joinpath(f'{prog_name}.yaml')
    if debug:
        print(f'Using config: {str(cfgfile.resolve())}')
    cfgobj = Munch.fromYAML(cfgfile.read_text(encoding=file_encoding))

    return cfgobj, cfgfile


def replace_angles(data):
    """
    Replace angle bracket with original curly brace.
    """
    data = re.sub(r'\s<{{\s', ' {{{ ', data)
    return re.sub(r'\}}>\s', '}}} ', data)


def replace_curlys(data):
    """
    Replace original outside curly brace with angle bracket.
    """
    data = re.sub(r'\s{{{\s', ' <{{ ', data)
    return re.sub(r'\}}}\s', '}}> ', data)


def restore_xml_comments(xmls):
    """
    Turn tagged comment elements back into xml comments.

    :param xmls: xml (file) output from ``unparse``
    :type xmls: str
    :return xmls: processed xml string
    :rtype: str
    """
    for rep in (("<#comment>", "<!-- "), ("</#comment>", " -->")):
        xmls = xmls.replace(*rep)
    return xmls


def sort_from_parent(input_data, prog_opts):
    """
    Sort a list based on whether the target sort key has a parent key.

    :param input_data: Dict obj representing YAML input data
    :param prog_opts: configuration options
    :type prog_opts: dict
    :return input_data: sorted input
    """
    # this should work for list/sublist structure
    is_sublist = prog_opts['has_parent_key']
    pkey_name = prog_opts['default_parent_key']
    skey_name = prog_opts['default_sort_key']
    pkey_list = input_data[pkey_name]

    if is_sublist:  # sort one or more sublists
        for i in range(len(pkey_list)):
            input_data[pkey_name][i][skey_name].sort()
    else:  # one top-level list
        input_data[skey_name].sort()

    return input_data


def text_file_reader(filepath, prog_opts):
    """
    Text file reader for specific data types plus raw text. Tries to handle
    YAML, JSON, CSV, and plain old text. Read and parse the file data if
    ``filepath`` is one of the expected types and return data objects. For
     all supported types of data, return a list of objects.

    :param filepath: filename/path as str
    :param prog_opts: configuration options
    :type prog_opts: dict
    :return object: file data as list
    :raises FileTypeError: if the input file is not xml or yml
    """
    data_in = {}
    infile = Path(filepath)

    if infile.suffix not in EXTENSIONS:
        raise FileTypeError("FileTypeError: unknown input file extension")
    with infile.open("r", encoding=prog_opts['file_encoding']) as file:
        if infile.suffix == '.csv':
            data_in = list(csv.DictReader(file))
        elif infile.suffix == '.json':
            data_in = json.load(file)
        elif infile.suffix in {'.yaml', '.yml'}:
            data_in = yaml_loader.safe_load(file)
        else:
            data_in = list(file.read().splitlines())

    return data_in
