'''Estimate how much you owe in taxes based on your CFDIs.'''
from pathlib import Path
import logging
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)


def get_cfdis(data_path):
    '''Load CFDIs from the data folder'''

    path = Path(data_path)
    files = [str(file) for file in path.rglob('*.xml') if file.is_file()]
    logging.info('FOUND %d CFDIs', len(files))

    for file in files:
        logging.info('Parsing %s', file)
        parse_cfdi(file)


def parse_cfdi(file):
    '''Parse a CFDI file'''
    try:
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml-xml')
            nomina_node = soup.find('nomina12:Nomina')
            if nomina_node and 'TotalPercepciones' in nomina_node.attrs:
                total_percepciones = float(nomina_node['TotalPercepciones'])
                logging.info('TotalPercepciones: %s', total_percepciones)
    except Exception as e:
        logging.error('Error parsing %s: %s', file, e)


if __name__ == "__main__":
    DATA_PATH = "data"
    get_cfdis(DATA_PATH)
