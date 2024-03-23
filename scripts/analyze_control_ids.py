"""
Simple ID string counter.
"""

import os
import sys
import typing
from collections import Counter, deque
from pathlib import Path

from fuzzy_match import match as fmatch

from ymltoxml.utils import get_filelist, text_file_reader

id_count: typing.Counter[str] = Counter()
result_queue = deque()

FILE = os.getenv('ID_FILE', default='tests/data/OE-expanded-profile-ids.txt')
FUZZY = os.getenv('FUZZY', default=None)
DEBUG = os.getenv('DEBUG', default=None)
SELFTEST = os.getenv('SELFTEST', default=None)
OPTIONS = {'file_encoding': 'utf-8'}
PROFILE_NAMES = ['HIGH', 'MODERATE', 'LOW', 'PRIVACY']


def get_profile_sets(dirpath='tests/data', filepattern='*.txt', debug=False):
    """
    Get the 800-53 oscal ID files and parse them into ID sets, return
    a list of sets. There should not be more than one controls file for
    each profile type.

    :Note: The oscal ID files are simply text files with a single "column"
           of ID strings extracted from the NIST oscal-content files or a
           CSV dump, etc. Samples are contained in the ``tests/data`` folder.

    :param dirpath: directory name to start file search
    :param filepattern: str of the form ``*.<ext>``
    :param debug: increase output verbosity
    :return: tuple of lists: (profile_sets, PROFILE_NAMES)
    """

    def get_profile_type(filename, debug=False):
        """
        Get oscal profile type from filename, where profile type is one of the
        exported profile names, ie, HIGH, MODERATE, LOW, or PRIVACY.
        """
        match = None

        if any((match := substring) in filename for substring in PROFILE_NAMES):
            if debug:
                print(f'Found profile type: {match}')

        return match

    h_set = set()
    m_set = set()
    l_set = set()
    p_set = set()

    nist_files = sorted(get_filelist(dirpath, filepattern, debug))

    for _, pfile in enumerate(nist_files):
        ptype = get_profile_type(pfile, debug)
        ptype_ids = text_file_reader(pfile, OPTIONS)
        t_set = set(sorted(ptype_ids))
        if ptype == 'HIGH':
            h_set.update(t_set)
        if ptype == 'MODERATE':
            m_set.update(t_set)
        if ptype == 'LOW':
            l_set.update(t_set)
        if ptype == 'PRIVACY':
            p_set.update(t_set)
        if ptype is None:
            if debug:
                print(f"{ptype} not found! Skipping...")
            break

    return [h_set, m_set, l_set, p_set], PROFILE_NAMES


if not Path(FILE).exists():
    print(f'Input file {FILE} not found!')
    sys.exit(1)

input_ids = list(Path(FILE).read_text(encoding='utf-8').splitlines())
in_set = set(input_ids)

print(f"Input control IDs -> {len(in_set)}")
if DEBUG:
    print(sorted(in_set))
if SELFTEST:
    id_sets, id_names = get_profile_sets('tests/data')
else:
    id_sets, id_names = get_profile_sets('800-53-control-ids/nist')

for id_set, ptype in zip(id_sets, id_names):
    print(f"\n{ptype} profile control IDs -> {len(id_set)}")

    print(f"Input set is in {ptype} set: {id_set > in_set}")
    common_set = sorted(id_set & in_set)
    print(f"Num input controls in {ptype} set -> {len(common_set)}")
    not_in_set = sorted(in_set - id_set)
    print(f"Num input controls not in {ptype} set -> {len(not_in_set)}")
    if DEBUG:
        print(f"Input controls not in {ptype} set: {not_in_set}")

print(f"\n{id_names[2]} set is in {id_names[0]} set: {id_sets[0] > id_sets[2]}")
print(f"{id_names[2]} set is in {id_names[1]} set: {id_sets[1] > id_sets[2]}")
print(f"{id_names[1]} set is in {id_names[0]} set: {id_sets[0] > id_sets[1]}")
print(f"{id_names[3]} set is in {id_names[0]} set: {id_sets[0] > id_sets[3]}")

not_in_high = sorted(in_set - id_sets[0])

if DEBUG:
    print("\nInput controls not in HIGH set\n")
    for ctl_id in not_in_high:
        print(ctl_id)

if FUZZY:
    print("Running fuzzy match for not-in HIGH set")
    print(f"  processing {len(not_in_high)} control IDs from not-in HIGH set")

    for ctl_id in not_in_high:
        result = fmatch.extract(ctl_id, id_sets[0], score_cutoff=0.6)
        match_list = [match for match in result if ctl_id.startswith(match[0])]
        if len(match_list) > 0:
            result_queue.append((ctl_id, match_list))

    print(f"\nFuzzy ID match shows {len(result_queue)} possible controls match HIGH set")

    if DEBUG:
        for match_res in result_queue:
            print(f"Ctl ID {match_res[0]} => {match_res[1]}")
