"""
Simple consumer test.
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

# read in some json "column data"
data = text_file_reader(FILE, OPTS)
if data[0].isupper():
    lc_ids = [xform_id(x) for x in data if len(x) > 0]

# spit out lowercase id format
for ctl in os_sorted(lc_ids):
    print(ctl)
