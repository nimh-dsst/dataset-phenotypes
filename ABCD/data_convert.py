import argparse
from pathlib import Path

import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=__doc__)
    parser.add_argument('-t', '--tabular-data', type=Path, action='store', dest='tab_data', metavar='TAB_DATA_DIR',
                        help='Path to directory with tabular data files in \'.txt\' format.')
    parser.add_argument('-d', '--dictionaries', type=Path, action='store', dest='dicts', metavar='DICTS_DIR',
                        default=Path('.'), help="Path to directory with data dictionaries in \'.csv\' format.")
    parser.add_argument('-o', '--output-dir', type=Path, action='store', dest='outdir', metavar='OUTPUT_DIR',
                        default=Path('.'), help="Destination directory for the \'.tsv\' formatted files.")
    args = parser.parse_args()

    return args.tab_data.resolve(), args.dicts.resolve(), args.outdir.resolve()


def data_summary(data_with_no_dict):
    print(f"A total of {len(data_with_no_dict)} data files don't have a corresponding data dictionary.")
    print(data_with_no_dict)


def main():
    # get command line arguments
    tab_data_dir, data_dict_dir, outdir = get_args()

    # extract nda short names into a list
    data_short_names = [i.name.split('.txt')[0] for i in
                        tab_data_dir.glob('*.txt')]  # assert that this is indeed a list of strings.
    data_dicts = list(data_dict_dir.glob('*.csv'))
    data_files_no_dict = []

    for d in data_short_names:
        expected_dict = data_dict_dir.joinpath(d + '.csv')  # constructing dictionary filename
        if expected_dict not in data_dicts:
            data_files_no_dict.append(d + '.txt')  # constructing data filename
        else:
            types_dict = {}  # dict of fields and data types
            dict_df = pd.read_csv(expected_dict)
            tsv_fields = dict_df['ElementName'].to_list()

            # type casting fields once it's read into a dataframe
            for col in tsv_fields:
                datatype = dict_df.loc[dict_df['ElementName'] == col, 'DataType'].values
                if datatype and datatype[0] == 'Integer':
                    types_dict[col] = 'Int64'
                elif datatype and datatype[0] == 'String':
                    types_dict[col] = 'str'

            data_df = pd.read_csv(tab_data_dir.joinpath(d + '.txt'), sep='\t', dtype=types_dict, skiprows=[1])
            # # print(types_dict)
            bids_data_df = data_df[tsv_fields]
            print(bids_data_df.head())
            # display(bids_data_df)
            # bids_data_df.to_csv(f"../dataset-phenotypes/ABCD/phenotype/{d + '.tsv'}", sep='\t',
            #                     quoting=csv.QUOTE_MINIMAL,
            #                     index=False)

    data_summary(data_files_no_dict)


if __name__ == '__main__':
    main()
