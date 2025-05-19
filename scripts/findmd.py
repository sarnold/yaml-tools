#!/usr/bin/env python

"""
Get the path to markdown files and print a comma-seprarted list of matches.
"""

from yaml_tools.utils import find_mdfiles

if __name__ == "__main__":

    target_files = find_mdfiles()
    if target_files:
        print(','.join(target_files))
