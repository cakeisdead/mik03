'''Estimate how much you owe in taxes based on your CFDIs.'''
from pathlib import Path
import logging
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


def get_cfdis(data_path):
    '''Load CFDIs from the data folder'''
    data = []
    path = Path(data_path)
    files = [str(file) for file in path.rglob('*.xml') if file.is_file()]
    logging.info('FOUND %d CFDIs', len(files))

    for file in files:
        logging.debug('Parsing %s', file)
        data.append(parse_cfdi(file))

    return data


def parse_cfdi(file):
    '''Parse a CFDI file'''
    # Initialize an empty dictionary to store CFDI data
    cfdi_data = {}

    try:
        with open(file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'lxml-xml')
            nomina_node = soup.find('nomina12:Nomina')
            if nomina_node and 'TotalPercepciones' in nomina_node.attrs:
                # NODO NOMINA
                total_percepciones = float(nomina_node['TotalPercepciones'])
                fecha_pago = nomina_node['FechaPago']

                # NODO PERCEPCIONES
                percepciones = soup.find('nomina12:Percepciones')
                total_sueldo = float(percepciones['TotalSueldos'])
                total_exento = float(percepciones['TotalExento'])
                total_gravado = float(percepciones['TotalGravado'])

                # NODO DEDUCCIONES
                deducciones = soup.find('nomina12:Deducciones')
                total_impuestos_retenidos = float(
                    deducciones['TotalImpuestosRetenidos'])

                # Datos Finales
                cfdi_data['fecha_pago'] = fecha_pago
                cfdi_data['total_percepciones'] = total_percepciones
                cfdi_data['total_sueldo'] = total_sueldo
                cfdi_data['total_exento'] = total_exento
                cfdi_data['total_gravado'] = total_gravado
                cfdi_data['total_impuestos_retenidos'] = total_impuestos_retenidos
    except Exception as e:
        logging.error('Error parsing %s: %s', file, e)

    return cfdi_data


if __name__ == "__main__":
    DATA_PATH = "data"  # Ruta en donde estan guardados los CFDIs en formato XML
    data = get_cfdis(DATA_PATH)

    # Totales
    if data:
        # Initialize aggregates
        total_percepciones = 0
        total_sueldo = 0
        total_exento = 0
        total_gravado = 0
        total_impuestos_retenidos = 0
        cfdi_count = 0

        # Sumarizar datos
        for cfdi in data:
            if cfdi:
                cfdi_count += 1
                total_percepciones += cfdi.get('total_percepciones', 0)
                total_sueldo += cfdi.get('total_sueldo', 0)
                total_exento += cfdi.get('total_exento', 0)
                total_gravado += cfdi.get('total_gravado', 0)
                total_impuestos_retenidos += cfdi.get(
                    'total_impuestos_retenidos', 0)

        # Print summary
        print(f"\nSummary of {cfdi_count} valid CFDIs:")
        print(f"Total Percepciones: ${total_percepciones:.2f}")
        print(f"Total Sueldos: ${total_sueldo:.2f}")
        print(f"Total Exento: ${total_exento:.2f}")
        print(f"Total Gravado: ${total_gravado:.2f}")
        print(f"Total Impuestos Retenidos: ${total_impuestos_retenidos:.2f}")
    else:
        print("No valid CFDI data found.")
