"""
ABIDE II phenotype data conversion from CSV to TSV format.

This script finds the data file as downloaded from http://www.nitrc.org/frs/downloadlink.php/4912 in .csv format and
converts it to .tsv format file to be in compliance with BIDS specification. The TSV files are deposited in the
`phenotype/` directory along with the data dictionary in JSON format.
"""


import pandas
import re
from pathlib import Path


# convert words and strings to exclusively alphanumerics for BIDS' sake
def bidsify(input_name):
    return re.sub(r'[\W_]+', '', input_name)


def data(input, output):
    for tabular_phenotype in ['ABIDEII_Composite_Phenotypic.csv', 'ABIDEII_Long_Composite_Phenotypic.csv']:
        # file path handling
        INPUT = input.joinpath(tabular_phenotype)
        OUTPUT = output.joinpath('phenotype', tabular_phenotype.replace('.csv', '.tsv'))
        status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)

        # Hard-coding minor changes to field names in phenotype file to match the one in the dictionary.json
        fieldname_changes = {
            "AGE_AT_SCAN ": "AGE_AT_SCAN"
        }

        df = pandas.read_csv(INPUT, keep_default_na=False, encoding='windows-1252')
        df.rename(fieldname_changes, axis=1, inplace=True)
        df.insert(0, 'participant_id', df['SUB_ID'].apply(lambda x: 'sub-' + bidsify(str(x))))
        df.to_csv(OUTPUT, sep='\t', index=False)

    return


def dictionary(_, output):
    # imports
    import json
    import os
    import shutil
    from copy import deepcopy


    # file path handling
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE.joinpath('fixed_dicts', 'ABIDEII_Data_Legend.tsv')
    OUTPUT = output.joinpath('phenotype', 'phenotype.json')
    status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)


    # read in the data dictionary
    data = pandas.read_csv(INPUT, sep='\t')

    # start the output dictionary
    data_dict = {
        "participant_id": {
            "LongName": "Participant Identifier",
            "Description": "Unique BIDS identifier for the participant in this study."
        },
        "SITE_ID": {
            "LongName": "ABIDE II Acquisition Site ID",
            "Description": "Site at which data were acquired.",
            "Levels": {
                "ABIDEII-BNI_1": "Barrow Neurological Institute",
                "ABIDEII-EMC_1": "Erasmus University Medical Center Rotterdam",
                "ABIDEII-ETH_1": "ETH Zürich",
                "ABIDEII-GU_1": "Georgetown University",
                "ABIDEII-IP_1": "Institut Pasteur and Robert Debré Hospital",
                "ABIDEII-IU_1": "Indiana University",
                "ABIDEII-KKI_1": "Kennedy Krieger Institute",
                "ABIDEII-KUL_3": "Katholieke Universiteit Leuven",
                "ABIDEII-NYU_1": "NYU Langone Medical Center: Sample 1",
                "ABIDEII-NYU_2": "NYU Langone Medical Center: Sample 2",
                "ABIDEII-OHSU_1": "Oregon Health and Science University",
                "ABIDEII-OILH_2": "Olin Neuropsychiatry Research Center, Institute of Living at Hartford Hospital",
                "ABIDEII-SDSU_1": "San Diego State University",
                "ABIDEII-SU_2": "Stanford University",
                "ABIDEII-TCD_1": "Trinity Centre for Health Sciences",
                "ABIDEII-UCD_1": "University of California Davis",
                "ABIDEII-UCLA_1": "University of California Los Angeles",
                "ABIDEII-USM_1": "University of Utah School of Medicine",
                "ABIDEII-U_MIA_1": "University of Miami"
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
            data_dict[ShortName] = {}
            data_dict[ShortName]["LongName"] = LongName
            data_dict[ShortName]["Description"] = Description
            if Levels:
                data_dict[ShortName]["Levels"] = Levels

        # manual corrections

        # delete erroneoues "Levels" entry
        del data_dict['HANDEDNESS_SCORES']['Levels']

        # fill in the "Description"
        data_dict['HANDEDNESS_SCORES']['Description'] = 'right handed: scores >= 50; left handed: scores <= -50; mixed handed: scores between -50 and 50, Type: Numeric, , Min: -100, Max: 100'

        # fill in the IQ "Levels"
        for IQ in ['FIQ', 'VIQ', 'PIQ']:
            # erroneoues "Levels" of only one of the IQ measurements
            del data_dict[IQ]['Levels']

            # fill in the "Description"
            data_dict[IQ]['Description'] = f'Type: Numeric, from {IQ}_TEST_TYPE'

            # fill in the "Description" into {IQ}_TEST_TYPE
            data_dict[f'{IQ}_TEST_TYPE']['Description'] = 'Type: String'

        # inject the correct "Levels" for {IQ}_TEST_TYPEs
        data_dict['VIQ_TEST_TYPE']['Levels'] = {
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
        data_dict['FIQ_TEST_TYPE']['Levels'] = deepcopy(data_dict['VIQ_TEST_TYPE']['Levels'])
        data_dict['FIQ_TEST_TYPE']['Levels']['KBIT-2'] = "Kaufman Brief Intellifence Test (KBIT-2)"

        # to save repetition, doing deepcopy of the same Levels, then adding Raven and SON-R
        data_dict['PIQ_TEST_TYPE']['Levels'] = deepcopy(data_dict['VIQ_TEST_TYPE']['Levels'])
        data_dict['PIQ_TEST_TYPE']['Levels']['Raven'] = "Raven's Progressive Matrices (Raven)"
        data_dict['PIQ_TEST_TYPE']['Levels']['SON-R'] = "Snijders-Oomen Nonverbal Intelligence (SON-R)"

        # pretty print it out into the output file
        f.write(json.dumps(data_dict, indent=4))

    phenotype_json_copy1 = str(OUTPUT.parent.joinpath('ABIDEII_Composite_Phenotypic.json'))
    phenotype_json_copy2 = str(OUTPUT.parent.joinpath('ABIDEII_Long_Composite_Phenotypic.json'))

    rename_status = os.rename(str(OUTPUT), phenotype_json_copy1)
    copy_status = shutil.copyfile(phenotype_json_copy1, phenotype_json_copy2)

    return
