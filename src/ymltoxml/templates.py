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
    if '(' in string:
        return string.replace('(', '.').replace(')', '').lower()
    else:
        slist = string.upper().split('.')
        if len(slist) == 2:
            return f'{slist[0]}({slist[1]})'
        elif len(slist) == 3:
            return f'{slist[0]}({slist[1]})({slist[2].lower()})'
        else:
            return f'{slist[0]}({slist[1]})({slist[2].lower()})({slist[3]})'


class Attachable(object):
    """
    A class that attaches all constructor named parameters as attributes.
    For example--

    >>> obj = Attachable(foo=42, size="of the universe")
    >>> repr(obj)
    "Attachable(foo=42, size='of the universe')"
    >>> obj.foo
    42
    >>> obj.size
    'of the universe'

    """

    def __init__(self, **kwargs):
        self.__args__ = kwargs
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            ", ".join("%s=%s" % (k, repr(v)) for k, v in self.__args__.items()),
        )
