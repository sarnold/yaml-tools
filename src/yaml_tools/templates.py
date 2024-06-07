"""
Template bits for generating SSG-style controls in YAML.
"""

import re

from .utils import pystache_render

PROFILES = ['LOW', 'MODERATE', 'HIGH', 'PRIVACY']

IMPACT_LVLS = ['low', 'moderate', 'high']

CTL_FIELD_MAP = {
    'id': 'Control Identifier',
    'name': 'Control (or Control Enhancement) Name',
    'notes': 'Discussion',
    'description': 'Control Text',
    'status': 'pending',
    'levels': None,
}

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
'''

ID_TEMPLATE = '''
controls:
  - id: {{caps}}
    status: {{status}}
    notes: |-
      {{notes}}
    rules: []
    description: |-
      {{description}}
    title: >-
      {{caps}} - {{name}}
    levels: []
'''


def generate_control(context):
    """
    Render an ID template string given a context dict.
    """
    id_yaml = pystache_render(ID_TEMPLATE, context)
    return id_yaml


def xform_id(string, strip_trailing_zeros=False):
    """
    Transform control ID string:

    AC-12(2) <==> ac-12.02
    """
    idp = re.compile(r'[)(-.]')  # regex character class for id separators
    str_list = [x for x in idp.split(string) if x != '']
    if strip_trailing_zeros:
        str_list = [x for x in idp.split(string) if x not in ('00', '')]

    if str_list[0].isupper():
        id_pfx = str_list[0].lower()
        id_num = int(str_list[1])
        if len(str_list) == 2:
            return f'{id_pfx}-{id_num:02d}'
        if len(str_list) > 2:
            id_num2 = int(str_list[2]) if str_list[2].isdigit() else str_list[2]
        if len(str_list) == 3:
            if str_list[2].isalpha():
                return f'{id_pfx}-{id_num:02d}.{id_num2}'
            return f'{id_pfx}-{id_num:02d}.{id_num2:02d}'
        if str_list[2].isalpha():
            return f'{id_pfx}-{id_num:02d}.{id_num2}.{str_list[3]}'
        return f'{id_pfx}-{id_num:02d}.{id_num2:02d}.{str_list[3]}'

    id_pfx = str_list[0].upper()
    id_num = int(str_list[1])
    if len(str_list) == 2:
        return f'{id_pfx}-{id_num:02d}'
    if len(str_list) > 2:
        id_num2 = int(str_list[2]) if str_list[2].isdigit() else str_list[2]
    if len(str_list) == 3:
        if str_list[2].isalpha():
            return f'{id_pfx}-{id_num:02d}({id_num2})'
        return f'{id_pfx}-{id_num:02d}({id_num2:02d})'
    if str_list[2].isalpha():
        return f'{id_pfx}-{id_num:02d}({id_num2})({str_list[3]})'
    return f'{id_pfx}-{id_num:02d}({id_num2:02d})({str_list[3]})'
