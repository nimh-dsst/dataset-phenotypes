"""ABIDE I phenotype data conversion from CSV to TSV format.

This script finds the data file as downloaded from http://www.nitrc.org/frs/downloadlink.php/4912 in .csv format and
converts it to .tsv format file to be in compliance with BIDS specification. The TSV files are deposited in the
`phenotype/` directory along with the data dictionary in JSON format.
"""

import argparse
import csv
from pathlib import Path

import pandas as pd


def help_text():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=__doc__)
    args = parser.parse_args()
    return args


def main():
    # calling help prompt
    help_text()

    # hard-coding file paths based on README instructions of dir organization
    data = Path('Phenotypic_V1_0b.csv')
    phenotype_dir = Path('phenotype')

    # Hard coding minor changes to field names in phenotype file to match the one in the dictionary.json
    fieldname_changes = {"ADI_RRB_TOTAL_C": "ADI_R_RRB_TOTAL_C", "ADOS_GOTHAM_SOCAFFECT": "ADOS_GOTHAM_SOC_AFFECT"}

    df = pd.read_csv(data, keep_default_na=False)
    df.rename(fieldname_changes, axis=1, inplace=True)
    df.to_csv(phenotype_dir / 'phenotype.tsv', sep='\t', quoting=csv.QUOTE_MINIMAL, index=False)


if __name__ == '__main__':
    main()
