#! /usr/bin/env python3


# imports
import json
import os
import pandas
from pathlib import Path

# file path handling
HERE = Path(__file__).parent.resolve()
INPUT_DIR = HERE.joinpath('nda_data_structure_definitions')
OUTPUT_DIR = HERE.joinpath('phenotype')
status = OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# make input list of CSV files
INPUTS = INPUT_DIR.glob('*.csv')

# loop over and enumerate input files
for j, INPUT in enumerate(INPUTS):

    # # debugging if statement with a print statement
    # if j in list(range(0, 50, 1)):
    #     print(j, INPUT.name)
    #     pass
    # else:
    #     continue

    # assign output file name for each iteration/INPUT of the loop
    OUTPUT = OUTPUT_DIR.joinpath(INPUT.name.replace('.csv', '.json'))

    # open the output file for writing
    with open(OUTPUT, 'w') as f:

        # start with an empty dictionary
        dictionary = {}

        # get the basename of the CSV file
        basename = INPUT.name.replace('.csv', '')

        # make sure the CSV is not empty (may be unnecessary)
        if os.stat(INPUT).st_size > 0:
            data = pandas.read_csv(INPUT)
        else:
            continue

        # loop over the rows of the CSV, one row = one field
        for i in range(data.shape[0]):

            # get the field name, a.k.a. "ShortName"
            try:
                ShortName = str(data['ElementName'][i])
            except:
                print('Skipping', str(i))
                continue

            # get the Description, and the "Notes" when present
            try:
                Description = str(data['ElementDescription'][i])
                Notes = str(data['Notes'][i])
                if Notes != 'nan':
                    Description += ' | ' + Notes
            except:
                Description = None

            # try to parse the Notes for Levels
            try:
                Notes = str(data['Notes'][i])
                
                # if the Notes are non-empty...
                if Notes != 'nan':

                    # start with an empty "Levels" dictionary
                    Levels = {}
                    
                    # strip off equal signs on the right and split by semi-colons
                    semicolons = Notes.rstrip('=').split(';')

                    # if there's more than one entry after splitting on semi-colons...
                    if len(semicolons) > 1:
                        # loop over the entries
                        for semicolon in semicolons:
                            # again, rstrip the right-most equal sign, but split on the equal signs after that
                            equals = semicolon.rstrip('=').split('=')

                            # if there's two entries it's "vanilla"
                            if len(equals) == 2:
                                coding = str(equals[0].strip())
                                meaning = str(equals[1].strip())
                                Levels[coding] = meaning

                            # if more than two AND the second entry has open and close square brackets...
                            elif len(equals) > 2 and '[' in equals[1] and ']' in equals[1]:
                                coding = str(equals[0].strip())
                                meaning = str(equals[1].split('[')[0].strip())
                                Levels[coding] = meaning

                            # if more than two AND the second entry has " / " in it...
                            elif len(equals) > 2 and ' / ' in equals[1]:
                                coding = str(equals[0].strip())
                                meaning = str(equals[1].split(' / ')[0].strip())
                                Levels[coding] = meaning

                            # if more than two AND the second entry has "/  " in it...
                            elif len(equals) > 2 and '/  ' in equals[1]:
                                coding = str(equals[0].strip())
                                meaning = str(equals[1].split('/  ')[0].strip())
                                Levels[coding] = meaning

                            # if more than two AND the second entry has " /(" in it...
                            elif len(equals) > 2 and ' /(' in equals[1]:
                                coding = str(equals[0].strip())
                                meaning = str(equals[1].split(' /(')[0].strip())
                                Levels[coding] = meaning

                            # if more than two AND the second entry has "//" in it...
                            elif len(equals) > 2 and '//' in equals[1]:
                                coding = str(equals[0].strip())
                                meaning = str(equals[1].split('//')[0].strip())
                                Levels[coding] = meaning

                            # if still more than two entries, then it's probably erroneous
                            elif len(equals) > 2:
                                print(basename, '|', ShortName, '| len(equals) > 2, the following is probably not a Level:', equals)

                            # otherwise there's only one entry and it's got to be erroneous
                            else:
                                print(basename, '|', ShortName, '| len(equals) < 2, the following single entry is being skipped:', equals)

                    # if there's only one entry after splitting on semi-colons, but splitting that one entry on the equal sign is length=2...
                    elif len(semicolons.split('=')) == 2:
                        coding, meaning = semicolons.split('=')
                        if coding != '' and meaning != '':
                            Levels[str(coding).strip()] = str(meaning).strip()
                        else:
                            print(ShortName, '| len(semicolons) == 1:', semicolons)

                    # otherwise something's wrong so just print the debugging info
                    else:
                        print(basename, '|', ShortName, '|', Notes)

                # if the Notes are empty, then just set Levels to None
                else:
                    Levels = None

            # if an exception happens, then just set Levels to None
            except:
                Levels = None

            # try to get the DataType
            try:
                DataType = str(data['DataType'][i])
            except:
                DataType = None

            # try to get the ValueRange range of possibilities
            try:
                ValueRange = str(data['ValueRange'][i])
                if ValueRange == 'nan':
                    ValueRange = None
            except:
                ValueRange = None

            # build the dictionary in the ShortName field
            dictionary[ShortName] = {}
            if Description:
                dictionary[ShortName]["Description"] = Description
            if DataType:
                dictionary[ShortName]["DataType"] = DataType
            if ValueRange:
                dictionary[ShortName]["ValueRange"] = ValueRange
            if Levels:
                dictionary[ShortName]["Levels"] = Levels

        # manual corrections, as necessary

        # dhx01 has a few odd entries that are just handled more simply here
        if basename == 'dhx01':
            dictionary['devhx_12_p']["Levels"]['999'] = "Don't know/No lo sé"
            del dictionary['devhx_18_p']['Levels']

        # genomics_sample03 has a field it's easier to just inject the Levels
        if basename == 'genomics_sample03' and ShortName == 'source_tissue':
            dictionary[ShortName]["Levels"] = {
                'ACC': 'anterior cingulate cortex (ACC)',
                'DLPFC': 'dorsolateral prefrontal cortex (DLPFC)',
                'CER': 'cerebellum (CER)',
                'dACC': 'dorsal anterior cingulate cortex (dACC)',
                'STG': 'superior temporal gyrus (STG)',
                'Dura': 'Dura mater (Dura)',
                'Hippo': 'Hippocampus (Hippo)'
            }

        # write out each data dictionary
        f.write(json.dumps(dictionary, indent=4))
