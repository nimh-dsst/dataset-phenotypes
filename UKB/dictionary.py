#! /usr/bin/env python


# imports
import json
import pandas
from pathlib import Path


# file path handling
HERE = Path(__file__).parent.resolve()
DATA = HERE.joinpath('Data_Dictionary_Showcase.tsv')
# CODINGS = HERE.joinpath('Codings.tsv')
DATACODE_DIR = HERE.joinpath('PHESANT-1.1', 'ukb_data_codes', 'data_codes')
OUTPUT = HERE.joinpath('phenotype', 'dictionary.json')
status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)


# read in the data dictionary and codings
data = pandas.read_csv(DATA, sep='\t')
# codings = pandas.read_csv(CODINGS, sep='\t')

# start the output dictionary
dictionary = {}

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
        dictionary[ShortName] = {}
        dictionary[ShortName]["LongName"] = LongName
        dictionary[ShortName]["Description"] = Description
        if Levels:
            dictionary[ShortName]["Levels"] = Levels
        if ValueType:
            dictionary[ShortName]["ValueType"] = ValueType
        if Units:
            dictionary[ShortName]["Units"] = Units
        if TermURL:
            dictionary[ShortName]["TermURL"] = TermURL

    # pretty print it out into the output file
    f.write(json.dumps(dictionary, indent=4))
