import csv
import json
from pathlib import Path

HERE = Path(__file__).parent.resolve()
OUTPUT_TSV = HERE.joinpath('dictionary_examples.tsv')
OUTPUT_JSON = HERE.joinpath('dictionary_examples.json')
PARENT = HERE.parent.resolve()

dictionaries = PARENT.glob('*/phenotype/*.json')

d = {}
for dictionary in dictionaries:
    # skip the NKI dictionaries for now
    if 'NKI' in str(dictionary):
        continue

    if 'HV' not in str(dictionary):
        continue

    with open(dictionary, 'r') as f:
        try:
            j = json.load(f)
        except json.decoder.JSONDecodeError:
            print('Skipping', dictionary)
            continue
    
    length = len(j.keys())
    if length > 3:
        first_quarter = length // 4
        halfway = length // 2
        third_quarter = halfway + first_quarter

        keys = list(j.keys())
        first_key = keys[first_quarter]
        middle_key = keys[halfway]
        last_key = keys[third_quarter]

        d[first_key] = j[first_key]
        d[middle_key] = j[middle_key]
        d[last_key] = j[last_key]

with open(OUTPUT_TSV, 'w', encoding='utf-8', newline = '') as o:
    fieldnames = ['Field', 'LongName', 'Description', 'Levels', 'Units', 'TermURL', 'HED']
    writer = csv.DictWriter(o, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    for field in d:
        field_dict = {'Field': field, 'LongName': '', 'Description': '', 'Levels': '', 'Units': '', 'TermURL': '', 'HED': ''}
        for key in d[field]:
            if key in fieldnames:
                if key == 'LongName':
                    field_dict['LongName'] = str(d[field][key])
                elif key == 'Description':
                    field_dict['Description'] = str(d[field][key])
                elif key == 'Levels':
                    levels = []
                    for level in d[field][key]:
                        levels.append(
                            ' = '.join([
                                str(level),
                                str(d[field][key][level]),
                                ])
                            )
                    field_dict['Levels'] = ' | '.join(levels)
                elif key == 'Units':
                    field_dict['Units'] = str(d[field][key])
                elif key == 'TermURL':
                    field_dict['TermURL'] = str(d[field][key])
                elif key == 'HED':
                    field_dict['HED'] = str(d[field][key])

        writer.writerow(field_dict)

with open(OUTPUT_JSON, 'w') as o:
    json.dump(d, o, indent=4)
