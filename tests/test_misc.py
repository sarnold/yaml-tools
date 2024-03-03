from pathlib import Path

import pytest
from munch import Munch

from ymltoxml.utils import (
    StrYAML,
    get_filelist,
    get_profile_sets,
    get_profile_type,
    load_config,
)

def test_get_filelist():
    test_path = Path('docs') / 'source' / 'index.rst'
    files = get_filelist('docs/source', '*.rst')
    assert isinstance(files, list)
    assert len(files) == 6
    assert str(test_path) in files


def test_get_filelist_debug():
    test_path = Path('docs') / 'source' / 'index.rst'
    files = get_filelist('docs/source', '*.rst', debug=True)
    assert isinstance(files, list)
    assert len(files) == 6
    assert str(test_path) in files


def test_get_profile_sets():
    dirpath = 'tests/data/'
    set_list = get_profile_sets(dirpath)
    assert len(set_list) == 4
    for item in set_list:
        assert isinstance(item, set)
    assert set_list[0] > set_list[1]


def test_get_profile_type():
    filename = 'PRIVACY-ids.txt'
    profile_type = get_profile_type(filename)
    assert isinstance(profile_type, str)
    assert profile_type == 'PRIVACY'


def test_get_profile_type_debug():
    filename = 'PRIVACY-ids.txt'
    profile_type = get_profile_type(filename, debug=True)
    assert isinstance(profile_type, str)
    assert profile_type == 'PRIVACY'


def test_str_dumper():
    my_yaml = StrYAML()
    assert isinstance(my_yaml, StrYAML)
    assert hasattr(my_yaml, 'dump')


def test_load_debug_config():
    popts, pfile = load_config(debug=True)

    assert isinstance(pfile, Path)
    assert isinstance(popts, Munch)
    assert hasattr(popts, 'default_xml_ext')
    assert pfile.stem == 'ymltoxml' or '.ymltoxml'


def test_load_ymltoxml_config():
    popts, pfile = load_config()

    assert isinstance(pfile, Path)
    assert isinstance(popts, Munch)
    assert hasattr(popts, 'default_xml_ext')
    assert pfile.stem == 'ymltoxml' or '.ymltoxml'


def test_load_yasort_config():
    popts, pfile = load_config(yasort=True)

    assert isinstance(pfile, Path)
    assert isinstance(popts, Munch)
    assert hasattr(popts, 'has_parent_key')
    assert pfile.stem == 'yasort' or '.yasort'
