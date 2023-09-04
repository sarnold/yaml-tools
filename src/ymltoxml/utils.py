"""
Shared utility code.
"""
import sys
from pathlib import Path

from munch import Munch
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.compat import StringIO

if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version

if sys.version_info < (3, 9):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

VERSION = version('ymltoxml')


class FileTypeError(Exception):
    """Raise when the file extension is not '.xml', '.yml', or '.yaml'"""

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


def load_config(file_encoding='utf-8', yasort=False, debug=False):
    """
    Load yaml configuration file and munchify the data. If local file is
    not found in current directory, the default will be loaded.

    :param file_encoding: file encoding of config file
    :type file_encoding: str
    :return: Munch cfg obj and cfg file as Path obj
    :rtype tuple:
    """
    prog_name = 'ymltoxml'
    if yasort:
        prog_name = 'yasort'
    defconfig = Path(f'.{prog_name}.yml')

    cfgfile = defconfig if defconfig.exists() else Path(f'.{prog_name}.yaml')
    if not cfgfile.exists():
        cfgfile = importlib_resources.files('ymltoxml.data').joinpath(f'{prog_name}.yaml')
    if debug:
        print(f'Using config: {str(cfgfile.resolve())}')
    cfgobj = Munch.fromYAML(cfgfile.read_text(encoding=file_encoding))

    return cfgobj, cfgfile


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


def sort_commented_map(commented_map):
    """
    Sort a ruamel.yaml commented map.

    :param commented_map: input data to sort
    :return cmap: sorted output data
    """
    cmap = CommentedMap()
    for key, value in sorted(commented_map.items()):
        if isinstance(value, CommentedMap):
            cmap[key] = sort_commented_map(value)
        elif isinstance(value, list):
            for i in enumerate(value):
                if isinstance(value[i[0]], CommentedMap):
                    value[i[0]] = sort_commented_map(value[i[0]])
            cmap[key] = value
        else:
            cmap[key] = value
    return cmap


def sort_from_parent(input_data, prog_opts, debug=False):
    """
    Parent key sort with not-quite-working CommentedSeq sorting.

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
        if prog_opts['process_comments']:
            root_comment = input_data.ca
            for i in range(len(pkey_list)):
                input_data = CommentedSeq(
                    sorted(input_data, key=lambda x: x[pkey_name][i][skey_name])
                )
                input_data._yaml_comment = root_comment
        else:
            for _ in range(len(pkey_list)):
                pkey_list[_][skey_name] = sorted(pkey_list[_][skey_name])
    else:  # one top-level list
        if prog_opts['process_comments']:
            root_comment = input_data.ca
            input_data = CommentedSeq(sorted(input_data, key=lambda x: x[skey_name]))
            input_data._yaml_comment = root_comment
        else:
            input_data[skey_name] = sorted(input_data[skey_name])

    return input_data
