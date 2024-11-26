"""
Simple consumer test with de-dup and sort.
"""

import os

from natsort import os_sorted

from yaml_tools.templates import xform_id
from yaml_tools.utils import text_file_reader

FILE = os.getenv('ID_FILE', default='tests/data/OE-expanded-profile-all-ids.txt')
OPTS = {
    'file_encoding': 'utf-8',
    'output_format': 'raw',
    'default_csv_hdr': None,
    'csv_delimiter': ';',
}


def set_unique(sequence):
    """
    Remove duplicates and emulate a set with ordered elements.
    """
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


# read in some json "column data"
data = text_file_reader(FILE, OPTS)

# we assume input IDs are classic upper case
raw_ids = [xform_id(x) for x in data if len(x) > 0]

unique_ids = set_unique(raw_ids)

# spit out lowercase id format
for ctl in os_sorted(unique_ids):
    print(ctl)
