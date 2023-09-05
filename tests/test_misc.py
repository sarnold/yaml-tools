from pathlib import Path

import pytest
from munch import Munch

from ymltoxml.utils import StrYAML, load_config


def test_str_dumper():
    my_yaml = StrYAML()
    assert isinstance(my_yaml, StrYAML)
    assert hasattr(my_yaml, 'dump')


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
