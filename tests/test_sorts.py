import sys

from munch import Munch
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

from ymltoxml.utils import StrYAML, sort_commented_map, sort_from_parent

cfg_str = """\
# comments should be preserved
file_encoding: 'utf-8'
default_yml_ext: '.yaml'
output_dirname: 'sorted-out'
default_parent_key: 'controls'
default_sort_key: 'rules'
has_parent_key: true
preserve_quotes: true
process_comments: true
mapping: 4
sequence: 6
offset: 4
"""

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

expected_sort_out = """\
policy: Security Requirements Guide - General Purpose Operating System
title: Security Requirements Guide - General Purpose Operating System
id: srg_gpos
version: v2r3
source: https://public.cyber.mil/stigs/downloads/
controls_dir: srg_gpos
levels:
    - id: high
    - id: medium
    - id: low
controls:  # sequences can have nodes that are mappings
    - id: Variables
      levels:
          - high
          - medium
          - low
      title: Variables
      rules:
          - login_banner_text=dod_banners  # this should be first
          - sshd_approved_ciphers=stig
          - sshd_approved_macs=stig
          - sshd_idle_timeout_value=10_minutes
          - var_account_disable_post_pw_expiration=35
          - var_accounts_authorized_local_users_regex=rhel8
          - var_auditd_action_mail_acct=root
          - var_auditd_space_left_action=email
          - var_auditd_space_left_percentage=25pc
          - var_authselect_profile=sssd
          - var_password_hashing_algorithm=SHA512
          - var_password_pam_dictcheck=1
          - var_sshd_disable_compression=no  # this should be last
"""


def recursive_sort_mappings(s):
    if isinstance(s, list):
        for elem in s:
            recursive_sort_mappings(elem)
        return
    if not isinstance(s, dict):
        return
    for key in sorted(s, reverse=True):
        value = s.pop(key)
        recursive_sort_mappings(value)
        s.insert(0, key, value)


# def find(key, dictionary):
#    # everything is a dict
#    for k, v in dictionary.items():
#        if k == key:
#            yield v
#        elif isinstance(v, dict):
#            for result in find(key, v):
#                yield result


def find(d, tag):
    if tag in d:
        yield d[tag]
    for k, v in d.items():
        if isinstance(v, dict):
            for i in find(v, tag):
                if isinstance(i, list):
                    for j in find(i, tag):
                        yield j


def lookup(sk, d, path=[]):
    # lookup the values for key(s) sk return as list the tuple (path to the value, value)
    if isinstance(d, dict):
        for k, v in d.items():
            if k == sk:
                yield (d, v)
            for res in lookup(sk, v, path + [k]):
                yield res
    elif isinstance(d, list):
        for item in d:
            for res in lookup(sk, item, path + [item]):
                yield res


yaml = YAML()
my_yaml = StrYAML()
data = yaml.load(yaml_str)
popts = yaml.load(cfg_str)

data_sorted = sort_from_parent(data, popts, True)
yaml.dump(data_sorted, sys.stdout)

# recursive_sort_mappings(data)
# yaml.dump(data, sys.stdout)
# out = sort_commented_map(data)
# yaml.dump(out, sys.stdout)

# for x in find(data, "rules"):
#     print(x)

# for d, value in lookup("rules", data):
# print(f'I got {d}')
# print(f'I got {value}')
