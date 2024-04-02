import pytest
from munch import Munch

import ymltoxml.oscal
from ymltoxml.oscal import process_data
from ymltoxml.utils import FileTypeError, StrYAML

defconfig_str = """\
# comments should be preserved
file_encoding: 'utf-8'
default_ext: '.yaml'
default_content_path: 'ext/oscal-content'
default_profile_path: 'nist.gov/SP800-53/rev5'
default_profile_name: 'PRIVACY'
default_ssg_glob: 'nist_ocp4.yml'
default_ssg_path: 'ext/content/controls'
default_lookup_key: 'controls'
input_format: null
output_format: 'json'
preserve_quotes: true
process_comments: false
mapping: 4
sequence: 6
offset: 4
"""

file_type_err = "FileTypeError: unknown input file extension"

yaml_str = """\
policy: NIST
title: Configuration Recommendations for Yocto- and OpenEmbedded-based Linux Variants
id: nist_openembedded
version: Revision 5
source: https://csrc.nist.gov/files/pubs/sp/800/53/r5/upd1/final/docs/sp800-53r5-control-catalog.xlsx
levels:
- id: low
- id: moderate
- id: high
controls:
- id: AC-11(1)
  status: pending
  notes: |-
    This can be a really long note.
  rules:
  - rule1
  - rule2
  description: |-
    A description of the control.
  title: >-
    AC-11(1) - CONTROL NAME
  levels:
  - high
  - moderate
- id: AC-12
  status: pending
  notes: |-
    Another really long note.
  rules:
  - rule3
  - rule4
  description: |-
    A description of another control.
  title: >-
    AC-12 - ANOTHER CONTROL NAME
  levels:
  - high
  - moderate
"""


def test_process_data(capfd, tmp_path):
    yaml = StrYAML()
    infile = 'tests/data/OE-expanded-profile-ids.txt'
    data_file = tmp_path / "test.yaml"
    data_file.write_text(yaml_str, encoding="utf-8")

    popts = yaml.load(defconfig_str)
    popts['default_ssg_path'] = tmp_path
    popts['default_ssg_glob'] = 'test.yaml'

    process_data(infile, popts)
    process_data(infile, popts, True)
    out, err = capfd.readouterr()
    print(out)
    assert 'Input control IDs' in out


def test_self_test(capfd):
    popts = Munch.fromYAML(defconfig_str)
    assert isinstance(popts, Munch)
    ymltoxml.oscal.self_test(popts)
    out, err = capfd.readouterr()
    print(out)
    assert 'Console tools' in out


def test_self_test_bad_file(capfd):
    yaml = StrYAML()
    cfg_dict = yaml.load(defconfig_str)

    cfg_dict['default_content_path'] = 'bogus/oscal'
    popts = Munch.fromDict(cfg_dict)
    assert isinstance(popts, Munch)
    ymltoxml.oscal.self_test(popts)
    out, err = capfd.readouterr()
    print(out)
    assert 'FileNotFoundError' in out


def test_self_test_bad_cfg(capfd):
    yaml = StrYAML()
    cfg_dict = yaml.load(defconfig_str)

    del cfg_dict['default_content_path']
    popts = Munch.fromDict(cfg_dict)
    ymltoxml.oscal.self_test(popts)
    out, err = capfd.readouterr()
    print(out)
    assert 'missing key' in out
