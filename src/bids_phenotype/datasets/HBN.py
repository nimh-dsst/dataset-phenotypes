"""
Child Mind Institute Healthy Brain Network tabular phenotype data and dictionary conversion to BIDS TSV and JSON files.
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
    import os
    import pandas
    from pathlib import Path
    import warnings
    import re

    warnings.simplefilter("ignore")

    # file path handling
    INPUT_DIR = input
    OUTPUT_DIR = output.joinpath('phenotype')
    status = OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    file_format = '.xlsx'

    # make input list of CSV files (and exclude does starting with ~)
    INPUTS = sorted(INPUT_DIR.glob(f'[!~]*{file_format}'))

    # loop over and enumerate input files
    for j, INPUT in enumerate(INPUTS):

        # assign output file name for each iteration/INPUT of the loop
        OUTPUT = OUTPUT_DIR.joinpath(INPUT.name.replace(f'{file_format}', '.json'))

        # open the output file for writing
        with open(OUTPUT, 'w') as f:

            # start the output dictionary
            data_dict = {
                "participant_id": {
                    "LongName": "Participant Identifier",
                    "Description": "Unique BIDS identifier for the participant in this study."
                }
            }

            # get the basename of the CSV file
            basename = INPUT.name.replace(f'{file_format}', '')
            print(basename)

            # make sure the CSV is not empty (may be unnecessary)
            if os.stat(INPUT).st_size > 0:
                with open(INPUT, 'rb') as handle:
                    # Ignore lines that do not have information
                    if basename == "ACE":
                        data = pandas.read_excel(handle, header=1, skiprows=[2])
                    elif basename in ["ACE_Boxed", "ACE_BRT", "ACE_Flanker", "ACE_SAAT", "ACE_Spatial_Span_B",
                                    "ACE_Spatial_Span_F"]:
                        # skip the last column from these questionnaires
                        data = pandas.read_excel(handle, header=1, skipfooter=1)
                    elif basename == 'ESWAN':
                        data = pandas.read_excel(handle, header=2)
                        # Set the Value Labels to the same in each question of the dictionary.
                        data.loc[2:, 'Value Labels'] = data.loc[2, 'Value Labels']
                    else:
                        data = pandas.read_excel(handle, header=1)
            else:
                continue

            # Specific transformations to the questionnaires done at the highest level
            # Merge columns from Response value on Diagnosis_KSADS
            if basename == 'Diagnosis_KSADS':
                # Merge the separate entries into one column
                data['Value Labels'] = data[
                    ['Response Values', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7']].apply(
                    lambda x: '; '.join(x[x.notnull()]), axis=1)

            elif basename == 'PreInt_FamHx':
                # All entries for the PreInt_FamHx should be saved separately for the following 6 categories.
                abbreviations = {
                                'm': 'mother',
                                'f': 'father',
                                's': 'sibling',
                                'p': 'child',
                                'o': 'other_relative'
                                }

            else:
                # For any questionnaire apart from PreInt_FamHx, we only go through the questionnaire once
                abbreviations = [1]

            for abbreviation in abbreviations:
                # loop over the rows of the CSV, one row = one field
                for i in range(data.shape[0]):

                    # get the field name, a.k.a. "Variable Name"
                    try:
                        ShortName = str(data['Variable Name'][i])
                    except:
                        try:
                            ShortName = str(data['Variable'][i])
                        except:
                            print('Skipping', str(i))
                            continue

                    # get the Description
                    try:
                        Description = str(data['Question'][i])
                    except:
                        try:
                            # Some files have "Description " (with an empty space at the end)
                            Description = str(data['Question '][i])
                        except:
                            try:
                                # Some files have "Item" instead fo "Question"
                                Description = str(data['Item'][i])
                            except:
                                try:
                                    # FFQ defines the Description as Score
                                    Description = str(data['Scores'][i])
                                except:
                                    Description = None
                    # Do some questionnaire specific transformation
                    if basename == 'Quotient_Ext':
                        if str(data['Description'][i]) != 'nan':
                            Description = Description + ". " + str(data['Description'][i])
                    # Do some cosmetics with the Description
                    if Description:
                        Description = Description.rstrip()
                        Description = Description.replace('\n', ' ')


                    # if there is no short name continue to the next row
                    if ShortName == 'nan':
                        # save the question for questions that depend on previous ones
                        Dependant = Description
                        continue

                    # get the Levels
                    try:
                        levels = str(data['Value Labels'][i])
                        if levels == '':
                            levels = levels.replace('', 'nan')

                        # transformation specific to questionnaires
                        if basename in ['Dishion_Teacher', 'KSADS_C', 'KSADS_P', 'PAQ_A']:
                            # remove commas as they might be interpreted as dividers between the levels
                            levels = levels.replace(', ', ' ')
                        elif basename == 'Diagnosis_KSADS':
                            # Merge the separate entries into one column
                            levels = levels.replace(';', ',')
                        elif basename == 'FFQ':
                            # Following instructions from the xlsx file, set value Labels for all frequency to the example
                            if ShortName.endswith('FREQ'):
                                levels = data['Value Labels'][3]
                        elif basename == 'FTQA':
                            # This questionnaire is a bit of a mess, some times "," and some times "\n" is used to separate the Value Labels
                            # Becase there are only a few entries, we manually change the entries where "," should not be used to
                            # split the levels
                            if ShortName in ['FTQA_06_A', 'FTQA_07_A']:
                                levels = levels.replace(',', ' ')
                        elif basename == 'PAQ_C':
                            # This questionnaire also mixes "," ans '\n' as spaces
                            if ShortName in ['PAQ_C_03', 'PAQ_C_04', 'PAQ_C_08']:
                                levels = levels.replace(',', ';')
                        elif basename == 'PBQ':
                            if ShortName in ['Relation', 'PBQ_03A', 'PBQ_04' ]:
                                levels = levels.replace(',', '  ')
                        elif basename in ['IAT', 'PCIAT', 'CELF']:
                            levels = levels.replace(';', ',')
                            #levels.strip("Severity Impairment Index:")
                            if ShortName in ['IAT_Total', 'Total Score']:
                                levels = re.split(r'^Severity Impairment Index: ', levels)[1]
                        elif basename == 'PreInt_Demos_Home':
                            if ShortName.startswith('living_'):
                                levels = levels.replace(',', ';')
                                Description = str(data['Question'][0])
                        elif basename == 'PreInt_DevHx':
                            if ShortName == 'newborn_problems':
                                levels = levels.replace(',', ';')
                        elif basename == 'PreInt_EduHx':
                            if ShortName == 'current_religious':
                                levels = levels.replace(',', '')
                        elif basename == 'PreInt_FamHx':
                            # Append information about which family member this entry correspond to
                            Description = f'{abbreviations[abbreviation]} - {Description}'
                            ShortName = ShortName.replace('[family member]', abbreviation)
                        elif basename == 'PreInt_FamHx_RDC':
                            if ShortName in ['fattsev', 'fattleth', 'mattsev', 'mattleth', 'sib1attsev', 'sib1attleth',
                                            'sib2attsev', 'sib2attleth', 'sib3attsev', 'sib3attleth', 'sib4attsev',
                                            'sib4attleth', 'sib5attsev', 'sib5attleth']:
                                levels = levels.replace(',', '')
                        elif basename in ['SWAN', 'SWAN ']:
                            levels = data['Value Labels'][0]

                    except:
                        # Some questionnaires use "Value Label" instead of "Value Labels"
                        try:
                            levels = str(data['Value Label'][i])
                            if basename == 'PPS':
                                if ShortName == 'PPS_M_Score':
                                    levels = levels.replace(',', '-')
                        except:
                            levels = None

                    # get levels
                    try:

                        # if the Notes are non-empty...
                        if levels != 'nan':

                            # start with an empty "Levels" dictionary
                            levels_dic = {}

                            # split by coma or new line depending on which questionnaire is being used
                            # Note: the space after the ',' is necessary to make sure that the numbers are not split in the FSQ
                            # questionnaire
                            splits = levels.split(', ')
                            if (len(splits) < 2):
                                # check if there are two = signs on the entry we are looking at
                                splits = levels.split('\n')

                            # if there's more than one entry after splitting the labels...
                            if len(splits) > 1:
                                # loop over the entries
                                for i_split in splits:
                                    # split on the equal signs after that
                                    equals = i_split.split('=')

                                    # if there's two entries it's "vanilla"
                                    if len(equals) == 2:
                                        coding = str(equals[0].strip())
                                        meaning = str(equals[1].strip())
                                        levels_dic[coding] = meaning

                            # if there's only one entry after splitting on semi-colons, but splitting that one entry on the equal sign is length=2...
                            elif len(splits) == 1:
                                splits = splits[0]

                                # split specific for questionnaire
                                if (re.match(r'SCARED_P_[A-Z]', ShortName)) or \
                                    (re.match(f'SCARED_SR_[A-Z]]', ShortName)):
                                    splits = re.split(r'(\d+)', splits)
                                    coding = splits[0] + splits[1]
                                    meaning = splits[2].rstrip()
                                    levels_dic[coding] = meaning
                                else:
                                    equals = splits.split('=')

                                    # if there's two entries it's "vanilla"
                                    if len(equals) == 2:
                                        coding = str(equals[0].strip())
                                        meaning = str(equals[1].strip())
                                        levels_dic[coding] = meaning

                            # otherwise something's wrong so just print the debugging info
                            else:
                                print(basename, '|', ShortName, '|')

                        # if the Notes are empty, then just set Levels to None
                        else:
                            levels_dic = None

                    # if an exception happens, then just set Levels to None
                    except:
                        levels_dic = None

                    # try to get the DataType
                    try:
                        DataType = str(data['Variable Type'][i])
                    except:
                        DataType = None


                    # try to get the ValueRange range of possibilities
                    try:
                        ValueRange = str(data['Values'][i])
                    except:
                        try:
                            ValueRange = str(data['Value'][i])
                        except:
                            ValueRange = None

                    if ValueRange == 'nan':
                        ValueRange = None
                    elif ValueRange:
                        # set new lines
                        ValueRange = ValueRange.replace('\n', '; ')

                    # build the dictionary in the ShortName field
                    data_dict[ShortName] = {}
                    if Description:
                        data_dict[ShortName]["Description"] = Description
                        del Description
                    if levels_dic:
                        data_dict[ShortName]["Levels"] = levels_dic
                        del levels_dic
                    if DataType:
                        data_dict[ShortName]["DataType"] = DataType
                        del DataType
                    if ValueRange:
                        data_dict[ShortName]["ValueRange"] = ValueRange
                        del ValueRange

                    # manual corrections, as necessary
                    if basename == "ACE_BRT":
                        data_dict[ShortName]["Description"] = data_dict[ShortName]["Description"].replace('\n', ' ')

            # write out each data dictionary
            f.write(json.dumps(data_dict, indent=4))

            # make sure that the important variables do not get passed to the next questionnaire

    return
