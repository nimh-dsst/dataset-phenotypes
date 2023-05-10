#! /usr/bin/env python3


# imports
import json
import pandas
from copy import deepcopy
from pathlib import Path


# file path handling
HERE = Path(__file__).parent.resolve()
INPUT = HERE.joinpath('ABIDE_LEGEND_V1.02.tsv')
OUTPUT = HERE.joinpath('phenotype', 'phenotype.json')
status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)


# read in the data dictionary
data = pandas.read_csv(INPUT, sep='\t')

# start the output dictionary
dictionary = {
    "SITE_ID": {
        "LongName": "ABIDE Acquisition Site ID",
        "Description": "Site at which data were acquired.",
        "Levels": {
            "CALTECH": "California Institute of Technology",
            "CMU": "Carnegie Mellon University",
            "KKI": "Kennedy Krieger Institute",
            "LEUVEN_1": "University of Leuven: Sample 1",
            "LEUVEN_2": "University of Leuven: Sample 2",
            "MAX_MUN": "Ludwig Maximilians University Munich",
            "NYU": "NYU Langone Medical Center",
            "OHSU": "Oregon Health and Science University",
            "OLIN": "Olin, Institute of Living at Hartford Hospital",
            "PITT": "University of Pittsburgh School of Medicine",
            "SBL": "Social Brain Lab, BCN NIC UMC Groningen, and Netherlands Institute for Neurosciences",
            "SDSU": "San Diego State University",
            "STANFORD": "Stanford University",
            "TRINITY": "Trinity Centre for Health Sciences",
            "UCLA_1": "University of California, Los Angeles: Sample 1",
            "UCLA_2": "University of California, Los Angeles: Sample 2",
            "UM_1": "University of Michigan: Sample 1",
            "UM_2": "University of Michigan: Sample 2",
            "USM": "University of Utah School of Medicine",
            "YALE": "Yale Child Study Center"
        }
    }
}

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

        if str(data['MIN'][i]) == '6.47':
            Description += ', Min: 6.47'
        elif str(data['MIN'][i]) != 'nan':
            Description += ', Min: ' + str(int(data['MIN'][i]))

        if str(data['MAX'][i]) != 'nan' and '≥' in data['MAX'][i]:
            Description += ', Max: >=' + str(int(data['MAX'][i].split('≥')[1]))
        elif str(data['MAX'][i]) != 'nan':
            Description += ', Max: ' + str(int(data['MAX'][i]))

        # get the field "Levels" from parsing semicolons and equal signs
        try:
            Levels = {}
            pairs = str(data['CODING SPECIFICATION'][i]).split('; ')

            for pair in pairs:
                pair_split = pair.split(' = ')
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

    # manual corrections to IQ measurements
    for IQ in ['FIQ', 'VIQ', 'PIQ']:
        # erroneoues "Levels" of only one of the IQ measurements
        del dictionary[IQ]['Levels']

        # fill in the "Description" into {IQ}_TEST_TYPE
        dictionary[IQ]['Description'] = f'Type: Numeric, from {IQ}_TEST_TYPE'

        # inject a simplified Description
        dictionary[f'{IQ}_TEST_TYPE']['Description'] = 'Type: String'

    # inject the correct "Levels" for {IQ}_TEST_TYPEs
    dictionary['FIQ_TEST_TYPE']['Levels'] = {
        "DAS_II_SA": "Differential Ability Scales II - School age (DAS-II)",
        "GIT": "Groninger Intelligence Test (GIT)",
        "HAWIK": "Hamburg-Wechsler Intelligence Test for Children (HAWIK-IV)",
        "WAIS_III": "Wechsler Adult Intelligence Scales (WAIS)",
        "WASI": "Wechsler Abbreviated Scales of Intelligence (WASI)",
        "WISC_III": "Wechsler Intelligence Scale for Children (WISC-III)",
        "WISC_III_DUTCH": "(Dutch) Wechsler Intelligence Scale for Children (WISC-III)",
        "WISC_IV_4_SUBTESTS": "Subtests of Wechsler Intelligence Scale for Children (WISC-IV)",
        "WISC_IV_FULL": "The full Wechsler Intelligence Scale for Children (WISC-IV)",
        "WST": "Wortschatztest (WST)"
    }

    # to save repetition, doing deepcopy of the same Levels, then adding PPVT
    dictionary['VIQ_TEST_TYPE']['Levels'] = deepcopy(dictionary['FIQ_TEST_TYPE']['Levels'])
    dictionary['VIQ_TEST_TYPE']['Levels']['PPVT'] = "Peabody Picture Vocabulary Test (PPVT)"

    # to save repetition, doing deepcopy of the same Levels, then adding RAVENS
    dictionary['PIQ_TEST_TYPE']['Levels'] = deepcopy(dictionary['FIQ_TEST_TYPE']['Levels'])
    dictionary['PIQ_TEST_TYPE']['Levels']['RAVENS'] = "Raven's Standard Progressive Matrices (RAVENS)"

    # pretty print it out into the output file
    f.write(json.dumps(dictionary, indent=4))
