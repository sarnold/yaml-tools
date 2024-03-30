"""
Simple consumer test.
"""

from ymltoxml.utils import text_data_writer, text_file_reader

OPTS = {
    'file_encoding': 'utf-8',
    'output_format': 'csv',
}


# read in some json "column data"
data = text_file_reader('tests/data/catalog.json', OPTS)
# spit out CSV records
ret = text_data_writer(data, OPTS)
