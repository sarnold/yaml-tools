"""
Template bits for generating SSG-style controls in YAML.
"""

import re
from typing import Dict, List

from .utils import pystache_render

PROFILES: List = ['LOW', 'MODERATE', 'HIGH', 'PRIVACY']

IMPACT_LVLS: List = ['low', 'moderate', 'high']

CTL_FIELD_MAP: Dict = {
    'id': 'Control Identifier',
    'name': 'Control (or Control Enhancement) Name',
    'notes': 'Discussion',
    'description': 'Control Text',
    'status': 'pending',
    'levels': None,
}

PREAMBLE: str = '''
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

ID_TEMPLATE: str = '''
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


def generate_control(context: Dict) -> str:
    """
    Render an ID template string given a context dict with key names for
    Control ID template fields, eg::

        'caps': 'AC-12(2)',
        'name': 'Control (or Control Enhancement) Name',
        'notes': 'Discussion',
        'description': 'Control Text',
        'status': 'pending',

    :param context: dict providing keys,values for ID_TEMPLATE fields
    :returns: yaml control ID string
    """
    id_yaml = pystache_render(ID_TEMPLATE, context)
    return id_yaml


def xform_id(string: str, strip_trailing_zeros: bool = False) -> str:
    """
    Transform control ID strings, add leading zeros in forward direction::

      AC-12(2) <==> ac-12.02

    Caller should filter zero-length input or handle IndexError as needed.

    :param string: id string in one of the above formats
    :param strip_trailing_zeros: off by default
    :returns: opposite ID format string
    """
    if string[0].isupper():
        idp = re.compile(r'[)(-]')  # regex character class id separators
        slist = [x for x in idp.split(string) if x != '']
        if strip_trailing_zeros:
            slist = [x for x in idp.split(string) if x not in ('00', '')]
        slist_with_dots = [slist[0].lower() + f"-{int(slist[1]):02d}"]
        slist_with_dots += [
            f".{s}" if s.isalpha() else f".{int(s):02d}" for s in slist[2:]
        ]
        new_id = ''.join(slist_with_dots)
    else:
        slist = string.upper().split('.')
        slist_with_parens = [slist[0]]
        slist_with_parens += [f"({s.lower()})" for s in slist[1:]]
        new_id = ''.join(slist_with_parens)
    return new_id
