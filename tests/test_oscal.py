import pytest
from munch import Munch

from ymltoxml.oscal import self_test
from ymltoxml.utils import FileTypeError, StrYAML

defconfig_str = """\
# comments should be preserved
file_encoding: 'utf-8'
default_yml_ext: '.yaml'
default_separator: '/'
default_oscal_dir: 'ext/oscal-content'
output_format: null
preserve_quotes: true
process_comments: false
mapping: 4
sequence: 6
offset: 4
"""

file_type_err = "FileTypeError: unknown input file extension"


def test_self_test(capfd):
    popts = Munch.fromYAML(defconfig_str)
    assert isinstance(popts, Munch)
    self_test(popts)
    out, err = capfd.readouterr()
    print(out)
    assert 'Console tools' in out


def test_self_test_bad_file(capfd):
    yaml = StrYAML()
    cfg_dict = yaml.load(defconfig_str)

    cfg_dict['default_oscal_dir'] = 'bogus/oscal'
    popts = Munch.fromDict(cfg_dict)
    assert isinstance(popts, Munch)
    self_test(popts)
    out, err = capfd.readouterr()
    print(out)
    assert 'FileNotFoundError' in out


def test_self_test_bad_cfg(capfd):
    yaml = StrYAML()
    cfg_dict = yaml.load(defconfig_str)

    del cfg_dict['default_oscal_dir']
    popts = Munch.fromDict(cfg_dict)
    self_test(popts)
    out, err = capfd.readouterr()
    print(out)
    assert 'missing key' in out
