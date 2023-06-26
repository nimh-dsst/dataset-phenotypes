"""
Nathan Kline Institute Rockland Sample tabular phenotype data and dictionary conversion to BIDS TSV and JSON files.
"""


import re
from pathlib import Path


# convert words and strings to exclusively alphanumerics for BIDS' sake
def bidsify(input_name):
    return re.sub(r'[\W_]+', '', input_name)


def data(input, output):

    return


def dictionary(input, output):
    # imports
    import json
    import pandas


    # file path handling
    INPUT_DIR = input
    OUTPUT_DIR = output.joinpath('phenotype')
    status = OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


    # make input list of CSV files
    INPUTS = INPUT_DIR.glob('*.csv')

    # loop over and enumerate input files
    for j, INPUT in enumerate(INPUTS):

        df = pandas.read_csv(INPUT)

        # assign output file name for each iteration/INPUT of the loop
        formname = INPUT.name.replace(' ', '_').replace('.csv', '.json')
        OUTPUT = OUTPUT_DIR.joinpath(str(formname))

        # open the output file for writing
        with open(OUTPUT, 'w') as f:

            # start with a single entry dictionary
            d = {
                "participant_id": {
                    "LongName": "Participant Identifier",
                    "Description": "Unique BIDS identifier for the participant in this study."
                }
            }

            current = ''
            for i, row in df.iterrows():
                # detecting if on first line of data dictionary/legend
                if current == '':
                    # start
                    ShortName = row['Question ID']
                    current = ShortName
                    LongName = row['Question Label']

                    if not pandas.isna(row['Question Description']) and not pandas.isna(row['Calculation Formula']):
                        Description = row['Question Description'] + ' | Calculation = ' + row['Calculation Formula']
                    elif not pandas.isna(row['Question Description']):
                        Description = row['Question Description']
                    elif not pandas.isna(row['Calculation Formula']):
                        Description = 'Calculation = ' + row['Calculation Formula']
                    else:
                        Description = None

                    Levels = None

                elif not pandas.isna(row['Question ID']):
                    # write
                    d[ShortName] = {}
                    d[ShortName]['LongName'] = LongName

                    if Description:
                        d[ShortName]['Description'] = Description

                    if Levels:
                        d[ShortName]['Levels'] = Levels

                    # reset
                    ShortName = row['Question ID']
                    LongName = row['Question Label']

                    if not pandas.isna(row['Question Description']) and not pandas.isna(row['Calculation Formula']):
                        Description = row['Question Description'] + ' | Calculation = ' + row['Calculation Formula']
                    elif not pandas.isna(row['Question Description']):
                        Description = row['Question Description']
                    elif not pandas.isna(row['Calculation Formula']):
                        Description = 'Calculation = ' + row['Calculation Formula']
                    else:
                        Description = None

                    Levels = None

                if not Levels and not pandas.isna(row['Response Value']):
                    Levels = { row['Response Value']: str(row['Response Label']) }
                elif Levels and not pandas.isna(row['Response Value']):
                    Levels[row['Response Value']] = str(row['Response Label'])

                # detecting if on last line of data dictionary/legend
                if i == df.shape[0] - 1:
                    # write
                    d[ShortName] = {}
                    d[ShortName]['LongName'] = LongName
                    if Description:
                        d[ShortName]['Description'] = Description
                    if Levels:
                        d[ShortName]['Levels'] = Levels

            with open(OUTPUT, 'w') as f:
                f.write(json.dumps(d, indent=4))

    return
