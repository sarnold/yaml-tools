"""
Simple SSG control ID matcher (ingests directly from content repo).
"""

import os
import sys
import typing
from collections import Counter
from pathlib import Path

from diskcache import Deque
from nested_lookup import nested_lookup

from ymltoxml.templates import xform_id
from ymltoxml.utils import get_cachedir, get_filelist, text_file_reader

id_count: typing.Counter[str] = Counter()
id_queue = Deque(get_cachedir(dir_name='id_queue'))
ctl_queue = Deque(get_cachedir(dir_name='ctl_queue'))

FILE = os.getenv('ID_FILE', default='tests/data/OE-expanded-profile-all-ids.txt')
SSG_PATH = os.getenv('SSG_PATH', default='ext/content/controls')
DEBUG = int(os.getenv('DEBUG', default=0))

OPTIONS = {'file_encoding': 'utf-8'}
FILE_GLOB = 'nist_*.yml'
CONTROL_FILES = [
    'nist_ocp4.yml',
    'nist_rhidm.yml',
    'nist_rhacm.yml',
    'nist_rhcos4.yml',
]


def set_unique(sequence):
    """
    Remove duplicates and emulate a set with ordered elements.
    """
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


if not Path(FILE).exists():
    print(f'Input file {FILE} not found!')
    sys.exit(1)

input_ids = Path(FILE).read_text(encoding='utf-8').splitlines()

if input_ids[0].islower():
    up_ids = [xform_id(x) for x in input_ids]
else:
    up_ids = input_ids

in_set = set(up_ids)

if DEBUG:
    print(f'Input Ids: {input_ids}')

id_queue.clear()
ctl_queue.clear()
if DEBUG:
    print(f'Id queue in {id_queue.directory}')
    print(f'Ctl queue in {ctl_queue.directory}')

ctl_files = get_filelist(SSG_PATH, FILE_GLOB, DEBUG)
nist_file_tuples = [(x, y) for x in ctl_files for y in CONTROL_FILES if y in x]

if DEBUG:
    print(f'SSG control files: {nist_file_tuples}')

for path in nist_file_tuples:
    print(f'Extracting IDs from {path[1]}')
    fpath = Path(path[0])

    try:
        indata = text_file_reader(fpath, OPTIONS)
    except FileTypeError as exc:
        print(f'{exc} => {fpath}')

    id_list = [x for x in nested_lookup('id', indata) if x.isupper()]
    id_queue.append((path[1], id_list))

    ctl_list = nested_lookup('controls', indata)[0]
    for ctl_id in ctl_list:
        ctl_queue.append((ctl_id['id'], ctl_id))

if DEBUG > 1:
    print(f'ID queue Front: {id_queue.peekleft()}')
    print(f'Control queue Front: {ctl_queue.peekleft()}')

print(f"\nInput control Ids -> {len(input_ids)}")
for _ in range(4):
    pname, id_list = id_queue.popleft()
    print(f"\n{pname} control IDs -> {len(id_list)}")
    id_set = set(id_list)

    print(f"Input set is in {pname} set: {id_set > in_set}")
    common_set = sorted(id_set & in_set)
    print(f"Num input controls in {pname} set -> {len(common_set)}")
    not_in_set = sorted(in_set - id_set)
    print(f"Num input controls not in {pname} set -> {len(not_in_set)}")
    if DEBUG:
        print(f"Input controls not in {pname} set: {not_in_set}")
