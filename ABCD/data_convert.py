"""ABCD tabular data conversion from TXT to TSV format.

This script finds the tabular data files as downloaded from NDA in .txt format and converts it to
.tsv format to be in compliance with BIDS specification. The TSV files are deposited in the `phenotype/`
directory along with data dictionaries in JSON format.
"""

import argparse
import csv
from pathlib import Path


def help_text():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=__doc__)
    args = parser.parse_args()
    return args


def data_summary(data_with_no_dict, dict_no_data_files):
    print(
        f"A total of {len(data_with_no_dict)} data files in the ABCD Release 4.0 tabular data package don't have a corresponding data dictionary.")
    print(data_with_no_dict)

    print(
        f"A total of {len(dict_no_data_files)} data dictionaries don't have a corresponding data file in the ABCD release 4.0 tabular data package.")
    print(dict_no_data_files)


def main():
    # calling help prompt
    help_text()

    # hard-coding file paths based on README instructions of dir organization
    tab_data_dir = Path('data')
    data_dict_dir = Path('nda_data_structure_definitions')
    outdir = Path('phenotype')

    # extract nda short names into a list
    data_files = list(tab_data_dir.glob('*.txt'))
    data_short_names = [i.stem for i in
                        data_files]  # assert that this is indeed a list of strings.
    data_dicts = list(data_dict_dir.glob('*.csv'))
    data_files_no_dict = []
    dict_no_data_files = []
    for data_dict in data_dicts:
        dict_prefix = data_dict.stem
        expected_data_file = tab_data_dir.joinpath(dict_prefix + '.csv')
        if expected_data_file not in data_files:
            dict_no_data_files.append(expected_data_file.name)

    for d in data_short_names:
        expected_dict = data_dict_dir.joinpath(d + '.csv')  # constructing dictionary filename
        # take stock of data files without their corresponding dictionaries
        if expected_dict not in data_dicts:
            data_files_no_dict.append(d + '.txt')  # constructing data filename

        # creating a list of lists where each sub-list is a formatted row
        rows = []
        curr_f = open(tab_data_dir.joinpath(d + '.txt'), 'r')
        for idx, line in enumerate(curr_f.readlines()):
            if idx != 1:  # skip over row describing fields
                line = ','.join(line.strip('\n').split('\t'))
                new_line = [word.strip('\"') for word in line.split(',') if not word == ""]
                rows.append(new_line)
        # writing the list of lists as a TSV file
        with open(outdir.joinpath(d + '.tsv'), 'w') as new_f:
            wr = csv.writer(new_f, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
            wr.writerows(rows)
    data_summary(data_files_no_dict, dict_no_data_files)


if __name__ == '__main__':
    main()
