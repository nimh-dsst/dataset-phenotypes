"""
UK Biobank tabular phenotype data and dictionary conversion to BIDS TSV and JSON files.
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
    DATA = input.joinpath('Data_Dictionary_Showcase.tsv')
    DATACODE_DIR = input.joinpath('PHESANT-1.1', 'ukb_data_codes', 'data_codes')
    OUTPUT = output.joinpath('phenotype', 'phenotype.json')
    status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)


    # read in the data dictionary
    data = pandas.read_csv(DATA, sep='\t')

    # start the output dictionary
    data_dict = {
        "participant_id": {
            "LongName": "Participant Identifier",
            "Description": "Unique BIDS identifier for the participant in this study."
        }
    }

    # open up the output file to write the dictionary into it far below
    with open(OUTPUT, 'w') as f:

        # for every row in the data dictionary
        for i in range(data.shape[0]):

            # get the ShortName from the "Field" column
            try:
                ShortName = str(data['Field'][i])
            except:
                continue

            # construct the LongName from the "Path" and "Category" columns
            try:
                LongName = '|'.join([ str(data['Path'][i]).replace(' > ', '|') + ' (Category ' + str(data['Category'][i]) + ')' ])
            except:
                continue

            # get the description from the "FieldID" column
            try:
                Description = 'FieldID ' + str(data['FieldID'][i]) + ': ' + str(data['Notes'][i])
            except:
                continue

            # get the field "Levels" from the codings and meanings
            try:
                Coding = str(int(data['Coding'][i]))
                datacode = pandas.read_csv(DATACODE_DIR.joinpath('datacode-' + Coding + '.tsv'), sep='\t')

                Levels = {}

                for coding, meaning in zip(datacode['coding'], datacode['meaning']):
                    Levels[str(coding)] = str(meaning)

            except:
                Levels = None

            # set the ValueType, NOTE: Not a valid BIDS sidecar JSON metadata field
            try:
                ValueType = str(data['ValueType'][i])
            except:
                ValueType = None

            # set the Units, NOTE: Not BIDS because of 185 unique unit types in UKB
            try:
                Units = str(data['Units'][i])
                # ignore "nan" Units
                if Units == 'nan':
                    Units = None
            except:
                Units = None

            # set the TermURL, when "Link" is present
            try:
                TermURL = str(data['Link'][i])
            except:
                TermURL = None

            # build the dictionary entry from the parsed values
            data_dict[ShortName] = {}
            data_dict[ShortName]["LongName"] = LongName
            data_dict[ShortName]["Description"] = Description
            if Levels:
                data_dict[ShortName]["Levels"] = Levels
            if ValueType:
                data_dict[ShortName]["ValueType"] = ValueType
            if Units:
                data_dict[ShortName]["Units"] = Units
            if TermURL:
                data_dict[ShortName]["TermURL"] = TermURL

        # pretty print it out into the output file
        f.write(json.dumps(data_dict, indent=4))

    return
