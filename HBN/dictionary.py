#! /usr/bin/env python3


# imports
import json
import os
import pandas
from pathlib import Path
import warnings

warnings.simplefilter("ignore")

# file path handling
HERE = Path(__file__).parent.resolve()
INPUT_DIR = HERE.joinpath('Data Dictionaries')
OUTPUT_DIR = HERE.joinpath('phenotype')
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

        # start with an empty dictionary
        dictionary = {}

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
                else:
                    data = pandas.read_excel(handle, header=1)
        else:
            continue

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
                        Description = None
            # If there
            if Description:
                Description = Description.rstrip()


            # if there is no short name continue to the next row
            if ShortName == 'nan':
                # save the question for questions that depend on previous ones
                Dependant = Description
                continue

            # get the Levels
            try:
                levels = str(data['Value Labels'][i])
            except:
                # Some questionnaires use "Value Label" instead of "Value Labels"
                try:
                    levels = str(data['Value Label'][i])
                except:
                    levels = None

            if basename == 'Dishion_Teacher':
                # remove commas as they might be interpreted as dividers between the levels
                levels = levels.replace(', ', ' ')

            # get levels
            try:

                # if the Notes are non-empty...
                if levels != 'nan':

                    # start with an empty "Levels" dictionary
                    levels_dic = {}

                    # split by coma or new line depending on which questionnaire is being used
                    splits = levels.split(',')
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
                    elif len(splits.split('=')) == 2:
                        coding, meaning = splits.split('=')
                        if coding != '' and meaning != '':
                            levels_dic[str(coding).strip()] = str(meaning).strip()
                        else:
                            print(ShortName, '| len(semicolons) == 1:', splits)

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

            # Merge columns from Response value on Diagnosis_KSADS
            if basename == 'Diagnosis_KSADS':
                # Merge the separate entries into one column
                data['Values'] = data[['Response Values', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7']].apply(
                    lambda x: '; '.join(x[x.notnull()]), axis=1)

            # try to get the ValueRange range of possibilities
            try:
                ValueRange = str(data['Values'][i])
            except:
                try:
                    ValueRange = str(data['Value'][i])
                except:
                    ValueRange = None

            # set new lines
            ValueRange = ValueRange.replace('\n', '; ')
            if ValueRange == 'nan':
                ValueRange = None

            # build the dictionary in the ShortName field
            dictionary[ShortName] = {}
            if Description:
                dictionary[ShortName]["Description"] = Description
                del Description
            if levels_dic:
                dictionary[ShortName]["Levels"] = levels_dic
                del levels_dic
            if DataType:
                dictionary[ShortName]["DataType"] = DataType
                del DataType
            if ValueRange:
                dictionary[ShortName]["ValueRange"] = ValueRange
                del ValueRange

            # manual corrections, as necessary
            if basename == "ACE_BRT":
                dictionary[ShortName]["Description"] = dictionary[ShortName]["Description"].replace('\n', ' ')

        # write out each data dictionary
        f.write(json.dumps(dictionary, indent=4))

        # make sure that the important variables do not get passed to the next questionnaire
