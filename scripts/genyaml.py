import xmltodict
import ruamel.yaml

from pathlib import Path


with open('in.xml', 'r+b') as xfile:
    payload = xmltodict.parse(xfile, process_comments=True)

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True  # type: ignore

pfile = Path('out.yaml')
yaml.dump(payload, pfile)
