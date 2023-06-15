"""ABIDE II phenotype data conversion from CSV to TSV format.

This script finds the data file as downloaded from http://www.nitrc.org/frs/downloadlink.php/4912 in .csv format and
converts it to .tsv format file to be in compliance with BIDS specification. The TSV files are deposited in the
`phenotype/` directory along with the data dictionary in JSON format.
"""

import pandas
from pathlib import Path

# file path handling
HERE = Path(__file__).parent.resolve()
INPUT = HERE.joinpath('ABIDEII_Composite_Phenotypic.csv')
OUTPUT = HERE.joinpath('phenotype', 'phenotype.tsv')
status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Hard coding minor changes to field names in phenotype file to match the one in the dictionary.json
fieldname_changes = {
    "AGE_AT_SCAN ": "AGE_AT_SCAN"
}

df = pandas.read_csv(INPUT, keep_default_na=False, encoding='windows-1252')
df.rename(fieldname_changes, axis=1, inplace=True)
df.to_csv(OUTPUT, sep='\t', index=False)
