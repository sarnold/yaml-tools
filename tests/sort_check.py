import sys

import ruamel.yaml

yaml_str = """\
f: 3
e:
- 10     # sequences can have nodes that are mappings
- 11
- x: A
  y: 30
  z:
    m: 51  # this should be last
    l: 50
    k: 49  # this should be first
d: 1
"""


def recursive_sort_mappings(s):
    if isinstance(s, list):
        for elem in s:
            recursive_sort_mappings(elem)
        return
    if not isinstance(s, dict):
        return
    for key in sorted(s, reverse=True):
        value = s.pop(key)
        recursive_sort_mappings(value)
        s.insert(0, key, value)


yaml = ruamel.yaml.YAML()
data = yaml.load(yaml_str)
recursive_sort_mappings(data)
yaml.dump(data, sys.stdout)
