import pytest

from ymltoxml.utils import FileTypeError, StrYAML
from ymltoxml.yagrep import process_inputs

defconfig_str = """\
# comments should be preserved
file_encoding: 'utf-8'
default_yml_ext: '.yaml'
default_separator: '/'
preserve_quotes: true
process_comments: false
mapping: 4
sequence: 6
offset: 4
"""

file_type_err = "FileTypeError: unknown input file extension"

yaml_str = """\
policy: Security Requirements Guide - General Purpose Operating System
title: Security Requirements Guide - General Purpose Operating System
id: srg_gpos
version: 'v2r3'
source: https://public.cyber.mil/stigs/downloads/
controls_dir: srg_gpos
levels:
- id: high
- id: medium
- id: low
controls:  # sequences can have nodes that are mappings
    -   id: Variables
        levels:
            - high
            - medium
            - low
        title: Variables
        rules:
            - var_sshd_disable_compression=no  # this should be last
            - var_password_hashing_algorithm=SHA512
            - var_password_pam_dictcheck=1
            - sshd_approved_macs=stig
            - sshd_approved_ciphers=stig
            - sshd_idle_timeout_value=10_minutes
            - var_accounts_authorized_local_users_regex=rhel8
            - var_account_disable_post_pw_expiration=35
            - var_auditd_action_mail_acct=root
            - var_auditd_space_left_percentage=25pc
            - var_auditd_space_left_action=email
            - login_banner_text=dod_banners  # this should be first
            - var_authselect_profile=sssd
"""


def test_process_inputs(capfd, tmp_path):
    yaml = StrYAML()
    inp = tmp_path / "in.yml"
    inp.write_text(yaml_str, encoding="utf-8")

    popts = yaml.load(defconfig_str)
    process_inputs(inp, 'low', popts)
    out, err = capfd.readouterr()


def test_process_inputs_debug(capfd, tmp_path):
    yaml = StrYAML()
    inp = tmp_path / "in.yml"
    inp.write_text(yaml_str, encoding="utf-8")

    popts = yaml.load(defconfig_str)
    process_inputs(inp, 'low', popts, True)
    out, err = capfd.readouterr()


def test_bad_file(capfd, tmp_path):
    yaml = StrYAML()
    popts = yaml.load(defconfig_str)
    inp2 = tmp_path / "in.ymml"
    inp2.write_text(yaml_str, encoding="utf-8")

    process_inputs(inp2, 'low', popts)
    out, err = capfd.readouterr()
    assert file_type_err in out
