#! /usr/bin/env python3


# imports
import json
import pandas
from copy import deepcopy
from pathlib import Path


# file path handling
HERE = Path(__file__).parent.resolve()
INPUT = HERE.joinpath('ABIDEII_Data_Legend.tsv')
OUTPUT = HERE.joinpath('phenotype', 'dictionary.json')
status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)


# read in the data dictionary
data = pandas.read_csv(INPUT, sep='\t')

# start the output dictionary
dictionary = {}

# open up the output file to write the dictionary into it far below
with open(OUTPUT, 'w') as f:

    # for every row in the data dictionary
    for i in range(data.shape[0]):

        # get the ShortName from the "COLUMN LABEL" column
        try:
            ShortName = str(data['COLUMN LABEL'][i])
        except:
            continue

        # get the LongName from the "DESCRIPTION" column
        try:
            LongName = str(data['DESCRIPTION'][i])
        except:
            continue

        # make the Description from "VARIABLE TYPE", "MIN", and "MAX" columns
        Description = 'Type: ' + str(data['VARIABLE TYPE'][i])

        if str(data['MIN'][i]).endswith('.0'):
            Description += ', Min: ' + str(int(data['MIN'][i]))
        elif str(data['MIN'][i]) != 'nan':
            Description += ', Min: ' + str(data['MIN'][i])

        if str(data['MAX'][i]).endswith('.0'):
            Description += ', Max: ' + str(int(data['MAX'][i]))
        elif str(data['MAX'][i]) != 'nan':
            Description += ', Max: ' + str(data['MAX'][i])

        # get the field "Levels" from parsing semicolons and equal signs
        try:
            Levels = {}
            pairs = str(data['CODING SPECIFICATION'][i]).split('; ')

            for pair in pairs:
                pair_split = pair.split('=')
                if len(pair_split) == 1 and pair_split[0] != 'nan':
                    Levels[pair_split[0]] = pair_split[0]
                else:
                    Levels[pair_split[0]] = pair_split[1]

        except:
            Levels = None

        # build the dictionary entry from the parsed values
        dictionary[ShortName] = {}
        dictionary[ShortName]["LongName"] = LongName
        dictionary[ShortName]["Description"] = Description
        if Levels:
            dictionary[ShortName]["Levels"] = Levels

    # manual corrections

    # delete erroneoues "Levels" entry
    del dictionary['HANDEDNESS_SCORES']['Levels']

    # fill in the "Description"
    dictionary['HANDEDNESS_SCORES']['Description'] = 'right handed: scores >= 50; left handed: scores <= -50; mixed handed: scores between -50 and 50, Type: Numeric, , Min: -100, Max: 100'

    # fill in the IQ "Levels"
    for IQ in ['FIQ', 'VIQ', 'PIQ']:
        # erroneoues "Levels" of only one of the IQ measurements
        del dictionary[IQ]['Levels']

        # fill in the "Description"
        dictionary[IQ]['Description'] = f'Type: Numeric, from {IQ}_TEST_TYPE'

        # fill in the "Description" into {IQ}_TEST_TYPE
        dictionary[f'{IQ}_TEST_TYPE']['Description'] = 'Type: String'

    # inject the correct "Levels" for {IQ}_TEST_TYPEs
    dictionary['VIQ_TEST_TYPE']['Levels'] = {
        "DAS": "Differential Ability Scale (DAS)",
        "DAS-II": "Differential Ability Scale II (DAS-II)",
        "WAIS-III": "Wechsler Adult Intelligence Scale III (WAIS-III)",
        "WAIS-IV": "Wechsler Adult Intelligence Scale IV (WAIS-IV)",
        "WAIS-IV-NL": "Wechsler Adult Intelligence Scale IV Dutch Language Version (WAIS-IV-NL)",
        "WASI": "Wechsler Abbreviated Scale of Intelligence (WASI)",
        "WASI-II": "Wechsler Abbreviated Scale of Intelligence II (WASI-II)",
        "WISC-III": "Wechsler Intelligence Scale of Children III (WISC-III)",
        "WISC-IV": "Wechsler Intelligence Scale of Children IV (WISC-IV)",
        "WPPSI-III": "Wechsler Preschool and Primary Scale of Intelligence III (WPPSI-III)"
    }

    # to save repetition, doing deepcopy of the same Levels, then adding KBIT-2
    dictionary['FIQ_TEST_TYPE']['Levels'] = deepcopy(dictionary['VIQ_TEST_TYPE']['Levels'])
    dictionary['FIQ_TEST_TYPE']['Levels']['KBIT-2'] = "Kaufman Brief Intellifence Test (KBIT-2)"

    # to save repetition, doing deepcopy of the same Levels, then adding Raven and SON-R
    dictionary['PIQ_TEST_TYPE']['Levels'] = deepcopy(dictionary['VIQ_TEST_TYPE']['Levels'])
    dictionary['PIQ_TEST_TYPE']['Levels']['Raven'] = "Raven's Progressive Matrices (Raven)"
    dictionary['PIQ_TEST_TYPE']['Levels']['SON-R'] = "Snijders-Oomen Nonverbal Intelligence (SON-R)"

    # pretty print it out into the output file
    f.write(json.dumps(dictionary, indent=4))
