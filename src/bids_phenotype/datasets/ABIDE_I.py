"""
ABIDE I tabular phenotype data conversion from CSV to TSV format.

This script finds the data file as downloaded from http://www.nitrc.org/frs/downloadlink.php/4912 in .csv format and
converts it to .tsv format file to be in compliance with BIDS specification. The TSV files are deposited in the
`phenotype/` directory along with the data dictionary in JSON format.
"""

import re
from pathlib import Path

# convert words and strings to exclusively alphanumerics for BIDS' sake
def bidsify(input_name):
    return re.sub(r'[\W_]+', '', input_name)


def data(input, output):

    import pandas

    # file path handling
    INPUT = input.joinpath('Phenotypic_V1_0b.csv')
    OUTPUT = output.joinpath('phenotype', 'phenotype.tsv')
    status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # Hard coding minor changes to field names in phenotype file to match the one in the dictionary.json
    fieldname_changes = {"ADI_RRB_TOTAL_C": "ADI_R_RRB_TOTAL_C", "ADOS_GOTHAM_SOCAFFECT": "ADOS_GOTHAM_SOC_AFFECT"}

    df = pandas.read_csv(INPUT, keep_default_na=False)
    df.rename(fieldname_changes, axis=1, inplace=True)
    df.insert(0, 'participant_id', df['SUB_ID'].apply(lambda x: 'sub-' + bidsify(str(x))))
    df.to_csv(OUTPUT, sep='\t', index=False)

    return


def dictionary(_, output):
    # imports
    import json
    import pandas
    from copy import deepcopy


    # file path handling
    HERE = Path(__file__).parent.resolve()
    INPUT = HERE.joinpath('fixed_dicts', 'ABIDE_LEGEND_V1.02.tsv')
    OUTPUT = output.joinpath('phenotype', 'phenotype.json')
    status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)


    # read in the data dictionary
    input_dict = pandas.read_csv(INPUT, sep='\t')

    # start the output dictionary
    output_dict = {
        "participant_id": {
            "LongName": "Participant Identifier",
            "Description": "Unique BIDS identifier for the participant in this study."
        },
        "SITE_ID": {
            "LongName": "ABIDE I Acquisition Site ID",
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
        for i in range(input_dict.shape[0]):

            # get the ShortName from the "COLUMN LABEL" column
            try:
                ShortName = str(input_dict['COLUMN LABEL'][i])
            except:
                continue

            # get the LongName from the "DESCRIPTION" column
            try:
                LongName = str(input_dict['DESCRIPTION'][i])
            except:
                continue

            # make the Description from "VARIABLE TYPE", "MIN", and "MAX" columns
            Description = 'Type: ' + str(input_dict['VARIABLE TYPE'][i])

            if str(input_dict['MIN'][i]) == '6.47':
                Description += ', Min: 6.47'
            elif str(input_dict['MIN'][i]) != 'nan':
                Description += ', Min: ' + str(int(input_dict['MIN'][i]))

            if str(input_dict['MAX'][i]) != 'nan' and '≥' in input_dict['MAX'][i]:
                Description += ', Max: >=' + str(int(input_dict['MAX'][i].split('≥')[1]))
            elif str(input_dict['MAX'][i]) != 'nan':
                Description += ', Max: ' + str(int(input_dict['MAX'][i]))

            # get the field "Levels" from parsing semicolons and equal signs
            try:
                Levels = {}
                pairs = str(input_dict['CODING SPECIFICATION'][i]).split('; ')

                for pair in pairs:
                    pair_split = pair.split(' = ')
                    if len(pair_split) == 1 and pair_split[0] != 'nan':
                        Levels[pair_split[0]] = pair_split[0]
                    else:
                        Levels[pair_split[0]] = pair_split[1]

            except:
                Levels = None

            # build the dictionary entry from the parsed values
            output_dict[ShortName] = {}
            output_dict[ShortName]["LongName"] = LongName
            output_dict[ShortName]["Description"] = Description
            if Levels:
                output_dict[ShortName]["Levels"] = Levels

        # manual corrections to IQ measurements
        for IQ in ['FIQ', 'VIQ', 'PIQ']:
            # erroneoues "Levels" of only one of the IQ measurements
            del output_dict[IQ]['Levels']

            # fill in the "Description" into {IQ}_TEST_TYPE
            output_dict[IQ]['Description'] = f'Type: Numeric, from {IQ}_TEST_TYPE'

            # inject a simplified Description
            output_dict[f'{IQ}_TEST_TYPE']['Description'] = 'Type: String'

        # inject the correct "Levels" for {IQ}_TEST_TYPEs
        output_dict['FIQ_TEST_TYPE']['Levels'] = {
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
        output_dict['VIQ_TEST_TYPE']['Levels'] = deepcopy(output_dict['FIQ_TEST_TYPE']['Levels'])
        output_dict['VIQ_TEST_TYPE']['Levels']['PPVT'] = "Peabody Picture Vocabulary Test (PPVT)"

        # to save repetition, doing deepcopy of the same Levels, then adding RAVENS
        output_dict['PIQ_TEST_TYPE']['Levels'] = deepcopy(output_dict['FIQ_TEST_TYPE']['Levels'])
        output_dict['PIQ_TEST_TYPE']['Levels']['RAVENS'] = "Raven's Standard Progressive Matrices (RAVENS)"

        # pretty print it out into the output file
        f.write(json.dumps(output_dict, indent=4))

    return
