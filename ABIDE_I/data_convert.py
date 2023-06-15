"""ABIDE I phenotype data conversion from CSV to TSV format.

This script finds the data file as downloaded from http://www.nitrc.org/frs/downloadlink.php/4912 in .csv format and
converts it to .tsv format file to be in compliance with BIDS specification. The TSV files are deposited in the
`phenotype/` directory along with the data dictionary in JSON format.
"""

import argparse
from pathlib import Path

import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=__doc__)
    parser.add_argument('input', type=Path, metavar='INPUT_FILE', required=True,
                        help='Path to the phenotype file in CSV format as downloaded from ABIDE I webpage.')
    parser.add_argument('output', type=Path, metavar='OUTPUT_DIR', required=False,
                        default=Path(__file__).parent, help='Path to output BIDS formatted directory.')
    args = parser.parse_args()
    return args


def main():

    args = get_args()
    data = args.input_file.resolve()
    phenotype_dir = args.output_dir.resolve() / 'phenotype'
    phenotype_dir.mkdir(parents=True, exist_ok=True)

    # Hard coding minor changes to field names in phenotype file to match the one in the dictionary.json
    fieldname_changes = {"ADI_RRB_TOTAL_C": "ADI_R_RRB_TOTAL_C", "ADOS_GOTHAM_SOCAFFECT": "ADOS_GOTHAM_SOC_AFFECT"}

    df = pd.read_csv(data, keep_default_na=False)
    df.rename(fieldname_changes, axis=1, inplace=True)
    df.to_csv(phenotype_dir / 'phenotype.tsv', sep='\t', index=False)


if __name__ == '__main__':
    main()
