"""
Simple ID string counter.
"""

import os
import sys
import typing
from collections import Counter
from pathlib import Path

from ymltoxml.utils import get_filelist, get_profile_type

id_count: typing.Counter[str] = Counter()
FILE = os.getenv('ID_FILE', default='tests/data/PRIVACY-ids-50.txt')
DEBUG = os.getenv('DEBUG', default=None)

if not Path(FILE).exists():
    print(f'Input file {FILE} not found!')
    sys.exit(1)

input_ids = list(Path(FILE).read_text(encoding='utf-8').splitlines())
i_set = set(sorted(input_ids))

print(f"Input control IDs -> {len(i_set)}")
if DEBUG:
    print(i_set)

nist_files = sorted(get_filelist('800-53-control-ids/nist', '*.txt', debug=DEBUG))

for pfile in nist_files:
    if not Path(pfile).exists():
        print(f"{pfile} profile not found! Skipping...")

    ptype = get_profile_type(pfile, debug=DEBUG)
    ptype_ids = list(Path(pfile).read_text(encoding='utf-8').splitlines())
    p_set = set(sorted(ptype_ids))
    print(f"\n{ptype} profile control IDs -> {len(p_set)}")

    print(f"Input set is in {ptype} set: {p_set > i_set}")
    common_set = p_set & i_set
    print(f"Num input controls in {ptype} set -> {len(common_set)}")
    not_in_set = i_set - p_set
    print(f"Num input controls not in {ptype} set -> {len(not_in_set)}")
    if DEBUG:
        print(f"Input controls not in {ptype} set: {not_in_set}")


#    id_count[pkt_type] += 1

# print("control ID counts:")
# for itype, count in id_count.items():
    # print(f"   {itype} -> {count}")
