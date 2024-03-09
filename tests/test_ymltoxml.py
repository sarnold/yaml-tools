import pytest

from ymltoxml.utils import StrYAML
from ymltoxml.ymltoxml import process_inputs

defconfig_str = """\
file_encoding: 'utf-8'
default_xml_ext: '.xml'
default_yml_ext: '.yaml'
process_comments: true
preserve_quotes: true
mapping: 2
sequence: 4
offset: 2
short_empty_elements: false
pretty: true
indent: '  '
"""


def test_process_inputs(xml_file, yml_file):
    yaml = StrYAML()
    popts = yaml.load(defconfig_str)

    process_inputs(xml_file, popts)
    process_inputs(yml_file, popts)


def test_process_inputs_debug(xml_file, yml_file):
    yaml = StrYAML()
    popts = yaml.load(defconfig_str)

    process_inputs(xml_file, popts, debug=True)
    process_inputs(yml_file, popts, debug=True)


def test_process_no_comments(xml_file, yml_file):
    yaml = StrYAML()
    popts = yaml.load(defconfig_str)
    popts['process_comments'] = False

    process_inputs(xml_file, popts)
    process_inputs(yml_file, popts)
