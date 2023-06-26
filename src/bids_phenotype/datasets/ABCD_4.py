"""
ABCD tabular data conversion from TXT to TSV format.

This script finds the tabular data files as downloaded from NDA in .txt format and converts it to
.tsv format to be in compliance with BIDS specification. The TSV files are deposited in the `phenotype/`
directory along with data dictionaries in JSON format.
"""


import csv
import re
from pathlib import Path


# convert words and strings to exclusively alphanumerics for BIDS' sake
def bidsify(input_name):
    return re.sub(r'[\W_]+', '', input_name)


def data_summary(data_without_dicts, dicts_without_data):
    print(
        f"A total of {len(data_without_dicts)} data files in the ABCD Release 4.0 tabular data package don't have a corresponding data dictionary.")
    print(data_without_dicts)

    print(
        f"A total of {len(dicts_without_data)} data dictionaries don't have a corresponding data file in the ABCD release 4.0 tabular data package.")
    print(dicts_without_data)


def data(input, output):
    print(__doc__)

    # hard-coding file paths based on README instructions of dir organization
    HERE = Path(__file__).parent.resolve()
    tab_data_dir = input
    data_dict_dir = HERE.joinpath('ABCD_4_nda_data_structure_definitions')
    outdir = output.joinpath('phenotype')
    status = outdir.parent.mkdir(parents=True, exist_ok=True)

    # extract nda short names into a list
    data_files = list(tab_data_dir.glob('*.txt'))
    data_short_names = [i.stem for i in
                        data_files]  # assert that this is indeed a list of strings.
    data_dicts = list(data_dict_dir.glob('*.csv'))

    data_files_no_dict = []
    dicts_without_data = []
    for data_dict in data_dicts:

        dict_prefix = data_dict.stem
        expected_data_file = tab_data_dir.joinpath(dict_prefix + '.csv')

        if expected_data_file not in data_files:
            dicts_without_data.append(expected_data_file.name)

    for d in data_short_names:
        expected_dict = data_dict_dir.joinpath(d + '.csv')  # constructing dictionary filename

        # take stock of data files without their corresponding dictionaries
        if expected_dict not in data_dicts:
            data_files_no_dict.append(d + '.txt')  # constructing data filename

        # creating a list of lists where each sub-list is a formatted row
        rows = []
        with open(tab_data_dir.joinpath(d + '.txt'), 'r') as curr_f:
            for idx, line in enumerate(curr_f.readlines()):
                if idx != 1:  # skip over row describing fields
                    no_newline = line.rstrip('\n')
                    new_line = [word.lstrip('"').rstrip('"') if not word == "" else "n/a" for word in
                                no_newline.split('\t')]
                    rows.append(new_line)

        # writing the list of lists as a TSV file
        with open(outdir.joinpath(d + '.tsv'), 'w') as new_f:
            wr = csv.writer(new_f, delimiter='\t')
            wr.writerows(rows)

    data_summary(data_files_no_dict, dicts_without_data)

    return


def dictionary(_, output):
    # imports
    import json
    import os
    import pandas
    from pathlib import Path

    # file path handling
    HERE = Path(__file__).parent.resolve()
    INPUT_DIR = HERE.joinpath('fixed_dicts', 'ABCD_4_nda_data_structure_definitions')
    OUTPUT_DIR = output.joinpath('phenotype')
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

            # start with a single entry dictionary
            data_dict = {
                "participant_id": {
                    "LongName": "Participant Identifier",
                    "Description": "Unique BIDS identifier for the participant in this study."
                }
            }

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
                data_dict[ShortName] = {}
                if Description:
                    data_dict[ShortName]["Description"] = Description
                if DataType:
                    data_dict[ShortName]["DataType"] = DataType
                if ValueRange:
                    data_dict[ShortName]["ValueRange"] = ValueRange
                if Levels:
                    data_dict[ShortName]["Levels"] = Levels

            # manual corrections, as necessary

            # dhx01 has a few odd entries that are just handled more simply here
            if basename == 'dhx01':
                data_dict['devhx_12_p']["Levels"]['999'] = "Don't know/No lo sé"
                del data_dict['devhx_18_p']['Levels']

            # genomics_sample03 has a field it's easier to just inject the Levels
            if basename == 'genomics_sample03' and ShortName == 'source_tissue':
                data_dict[ShortName]["Levels"] = {
                    'ACC': 'anterior cingulate cortex (ACC)',
                    'DLPFC': 'dorsolateral prefrontal cortex (DLPFC)',
                    'CER': 'cerebellum (CER)',
                    'dACC': 'dorsal anterior cingulate cortex (dACC)',
                    'STG': 'superior temporal gyrus (STG)',
                    'Dura': 'Dura mater (Dura)',
                    'Hippo': 'Hippocampus (Hippo)'
                }

            # write out each data dictionary
            f.write(json.dumps(data_dict, indent=4))

    return
