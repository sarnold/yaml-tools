"""
Simple ID string counter.
"""

import os
import sys
import typing
from collections import Counter
from pathlib import Path

from ymltoxml.utils import get_profile_sets

id_count: typing.Counter[str] = Counter()
FILE = os.getenv('ID_FILE', default='tests/data/PRIVACY-ids.txt')
DEBUG = os.getenv('DEBUG', default=None)
SELFTEST = os.getenv('SELFTEST', default=None)

if not Path(FILE).exists():
    print(f'Input file {FILE} not found!')
    sys.exit(1)

input_ids = list(Path(FILE).read_text(encoding='utf-8').splitlines())
in_set = set(sorted(input_ids))

print(f"Input control IDs -> {len(in_set)}")
if DEBUG:
    print(in_set)
if SELFTEST:
    id_sets, id_names = get_profile_sets('tests/data')
else:
    id_sets, id_names = get_profile_sets('800-53-control-ids/nist')

for id_set, ptype in zip(id_sets, id_names):
    print(f"\n{ptype} profile control IDs -> {len(id_set)}")

    print(f"Input set is in {ptype} set: {id_set > in_set}")
    common_set = id_set & in_set
    print(f"Num input controls in {ptype} set -> {len(common_set)}")
    not_in_set = in_set - id_set
    print(f"Num input controls not in {ptype} set -> {len(not_in_set)}")
    if DEBUG:
        print(f"Input controls not in {ptype} set: {not_in_set}")

print(f"\n{id_names[2]} set is in {id_names[0]} set: {id_sets[0] > id_sets[2]}")
print(f"{id_names[2]} set is in {id_names[1]} set: {id_sets[1] > id_sets[2]}")
print(f"{id_names[1]} set is in {id_names[0]} set: {id_sets[0] > id_sets[1]}")
print(f"{id_names[3]} set is in {id_names[0]} set: {id_sets[0] > id_sets[3]}")
