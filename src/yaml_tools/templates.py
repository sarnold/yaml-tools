"""
Template bits for generating SSG-style controls in YAML.
"""

from .utils import pystache_render

PREAMBLE = '''
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
'''

ID_TEMPLATE = '''
- id: {{caps}}
  status: {{status}}
  notes: |-
    {{notes}}
  rules: {{rules_list}}
  description: |-
    {{description}}
  title: >-
    {{caps}} - {{name}}
  levels: {{levels_list}}
'''


def generate_control(context):
    """
    Render an ID template string given a context dict.
    """
    id_yaml = pystache_render(ID_TEMPLATE, context)
    return id_yaml


def xform_id(string):
    """
    Transform control ID string:

    AC-12(2) <==> ac-12.2
    """
    if '(' in string or string.isupper():
        return string.replace('(', '.').replace(')', '').lower()

    slist = string.upper().split('.')
    if len(slist) == 1:
        return slist[0]
    if len(slist) == 2:
        return f'{slist[0]}({slist[1]})'
    if len(slist) == 3:
        return f'{slist[0]}({slist[1]})({slist[2].lower()})'
    return f'{slist[0]}({slist[1]})({slist[2].lower()})({slist[3]})'
