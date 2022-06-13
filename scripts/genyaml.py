import sys
import json
import xmltodict
import ruamel.yaml

from pathlib import Path
from pprint import pprint


with open('in.xml', 'r+b') as xfile:
    payload = xmltodict.parse(xfile, process_comments=True)

#print(json.dumps(payload, indent=2))
#pprint(payload)

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True

pfile = Path('out.yaml')
yaml.dump(payload, pfile)
