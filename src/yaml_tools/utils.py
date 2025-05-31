"""
Shared utility code.
"""

import collections
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pystache
import yaml as yaml_loader
from munch import Munch
from natsort import os_sorted
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

EXTENSIONS = ['.csv', '.json', '.rst', '.tmpl', '.txt', '.yaml', '.yml']
PROFILE_ID_FILES = [
    'HIGH-ids.txt',
    'MODERATE-ids.txt',
    'LOW-ids.txt',
    'PRIVACY-ids.txt',
]
PROFILE_NAMES = ['HIGH', 'MODERATE', 'LOW', 'PRIVACY']
VERSION = version('yaml_tools')


class FileTypeError(Exception):
    """
    Raise when the file extension is not '.xml', '.yml', or '.yaml'.
    """

    __module__ = Exception.__module__


class SortedSet(collections.abc.Set):
    """
    Alternate set implementation favoring space over speed, while not
    requiring the set elements to be hashable. We also add a sort method.
    """

    def __init__(self, iterable):
        self.elements: List = []
        for value in iterable:
            if value not in self.elements:
                self.elements.append(value)

    def __iter__(self):
        return iter(self.elements)

    def __contains__(self, value):
        return value in self.elements

    def __len__(self):
        return len(self.elements)

    def sort(self):
        """Why not be sorted?"""
        return sorted(self.elements)

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))


class StrYAML(YAML):
    """
    New API likes dumping straight to file/stdout, so we subclass and
    create 'inefficient' custom string dumper.
    """

    def dump(self, data, stream=None, **kw):
        stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        return stream.getvalue()


def get_filelist(dirpath: str, filepattern: str = '*.txt', debug: bool = False) -> List:
    """
    Get path objects matching ``filepattern`` starting at ``dirpath`` and
    return a list of matching paths for any files found.

    :param dirpath: directory to start file search
    :param filepattern: file extension glob
    :param debug: increase output verbosity
    """
    file_list: List = []
    filenames = Path(dirpath).rglob(filepattern)
    for pfile in list(filenames):
        file_list.append(str(pfile))
    if debug:
        print(f'Found file list: {file_list}')
    return file_list


def get_profile_ids(prog_opts: Dict, debug: bool = False) -> List[str]:
    """
    Replacement for ``get_filelist()`` when using the NIST profile ID text
    files (which are now packaged with the YAML config files).
    """
    id_str_data: List = []
    id_data = importlib_resources.files('yaml_tools').joinpath('data')
    for file in PROFILE_ID_FILES:
        ptype = get_profile_type(file, debug=debug)
        pdata = os_sorted(
            id_data.joinpath(file)
            .read_text(encoding=prog_opts['file_encoding'])
            .splitlines()
        )
        id_str_data.append((ptype, pdata))
    return id_str_data


def get_profile_type(filename: str, debug: bool = False) -> str:
    """
    Get oscal profile type from filename, where profile type is one of the
    exported profile names, ie, HIGH, MODERATE, LOW, or PRIVACY.
    """
    pmatch: str = ''
    for x in PROFILE_NAMES:
        if x in filename:
            pmatch = x
            if debug:
                print(f'Found profile type: {pmatch}')
    return pmatch


def load_config(
    prog_name: str = 'ymltoxml',
    pkg: str = 'yaml_tools.data',
    file_encoding: str = 'utf-8',
    debug: bool = False,
) -> Tuple[Munch, Path]:
    """
    Load yaml configuration file and munchify the data. If local file is
    not found in current directory, the default will be loaded.

    :param prog_name: filename of calling script (no extension)
    :param pkg: name of calling package.path for importlib
    :param file_encoding: file encoding of config file
    :param debug: enable extra processing info
    """
    defconfig = Path(f'.{prog_name}.yml')

    cfgfile = defconfig if defconfig.exists() else Path(f'.{prog_name}.yaml')
    if not cfgfile.exists():
        file_ref = importlib_resources.files(pkg).joinpath(f'{prog_name}.yaml')
        with importlib_resources.as_file(file_ref) as path:
            cfgfile = path
    if debug:
        print(f'Using config: {str(cfgfile.resolve())}')
    cfgobj = Munch.fromYAML(cfgfile.read_text(encoding=file_encoding))  # type: ignore

    return cfgobj, cfgfile


def pystache_render(*args, **kwargs) -> Any:
    """
    Render pystache template with strict mode enabled.
    """
    render = pystache.Renderer(missing_tags='strict')
    return render.render(*args, **kwargs)


def replace_angles(data: str) -> str:
    """
    Replace angle bracket with original curly brace.
    """
    data = re.sub(r'\s<{{\s', ' {{{ ', data)
    return re.sub(r'\}}>\s', '}}} ', data)


def replace_curlys(data: str) -> str:
    """
    Replace original outside curly brace with angle bracket.
    """
    data = re.sub(r'\s{{{\s', ' <{{ ', data)
    return re.sub(r'\}}}\s', '}}> ', data)


def restore_xml_comments(xmls: str) -> str:
    """
    Turn tagged comment elements back into xml comments.

    :param xmls: xml (file) output from ``unparse``
    :returns: processed xml string
    """
    for rep in (("<#comment>", "<!-- "), ("</#comment>", " -->")):
        xmls = xmls.replace(*rep)
    return xmls


def sort_from_parent(input_data: Dict, prog_opts: Dict) -> Dict:
    """
    Sort a list based on whether the target sort key has a parent key.

    :param input_data: Dict obj representing YAML input data
    :param prog_opts: configuration options
    :returns: sorted input
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


def str_yaml_dumper(data: Dict, prog_opts: Dict) -> Any:
    """
    Small StrYAML() dump wrapper.
    """
    yaml = StrYAML()
    yaml.indent(
        mapping=prog_opts['mapping'],
        sequence=prog_opts['sequence'],
        offset=prog_opts['offset'],
    )
    yaml.preserve_quotes = prog_opts['preserve_quotes']
    return yaml.dump(data)


def text_data_writer(outdata: Dict, prog_opts: Dict):
    """
    Text data writer with optional formatting (default is raw); uses config
    setting for output format. Supports the same text data formats supported
    by the ``text_file_reader()`` input function:

    * csv
    * json
    * yaml
    * raw

    Sends formatted data to stdout; redirect to a file as needed.

    :param outdata: data to be written to stdout
    :param prog_opts: configuration options
    """
    out = ''
    csv_hdr = prog_opts['default_csv_hdr']
    delim = prog_opts['csv_delimiter'] if prog_opts['csv_delimiter'] else ';'
    fmt = prog_opts['output_format'] if prog_opts['output_format'] else 'raw'

    if fmt == 'csv' and isinstance(outdata, collections.abc.Sequence):
        field_names = csv_hdr if csv_hdr else list(outdata[0].keys())
        w = csv.DictWriter(sys.stdout, field_names, delimiter=delim)
        w.writeheader()
        w.writerows(outdata)

    else:
        if fmt == 'json':
            out = json.dumps(outdata, indent=4, sort_keys=True)
        elif fmt == 'yaml':
            out = str_yaml_dumper(outdata, prog_opts)
        else:
            out = repr(outdata)

        sys.stdout.write(out + '\n')


def text_file_reader(file: Path, prog_opts: Dict) -> Any:
    """
    Text file reader for specific data types including raw text. Tries
    to handle YAML, JSON, CSV, text files with IDs, and plain ASCII
    text. Read and parse the file data if ``file`` is one of the
    expected types and return data objects. For all supported types of
    data, return a dictionary (or a list if input is a sequence).

    :param file: filename/path to read
    :param prog_opts: configuration options
    :returns: file data as dict or list
    :raises FileTypeError: if input file extension is not in EXTENSIONS
    """
    data_in: Any
    infile = Path(file)
    delim = prog_opts['csv_delimiter'] if prog_opts['csv_delimiter'] else ';'

    if infile.suffix not in EXTENSIONS:
        msg = f"invalid input file extension: {infile.name}"
        raise FileTypeError(msg)
    with infile.open("r", encoding=prog_opts['file_encoding']) as dfile:
        if infile.suffix == '.csv':
            data_in = list(csv.DictReader(dfile, delimiter=delim))
        elif infile.suffix == '.json':
            data_in = json.load(dfile)
        elif infile.suffix in {'.yaml', '.yml'}:
            data_in = yaml_loader.safe_load(dfile)
        elif 'ids' in infile.name and infile.suffix == '.txt':
            data_in = list(dfile.read().splitlines())
        else:
            data_in = dfile.readlines()

    return data_in
