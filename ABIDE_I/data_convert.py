"""ABIDE I phenotype data conversion from CSV to TSV format.

This script finds the data file as downloaded from http://www.nitrc.org/frs/downloadlink.php/4912 in .csv format and
converts it to .tsv format file to be in compliance with BIDS specification. The TSV files are deposited in the
`phenotype/` directory along with the data dictionary in JSON format.
"""

import pandas as pd
from pathlib import Path

# file path handling
HERE = Path(__file__).parent.resolve()
INPUT = HERE.joinpath('Phenotypic_V1_0b.csv')
OUTPUT = HERE.joinpath('phenotype', 'phenotype.tsv')
status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Hard coding minor changes to field names in phenotype file to match the one in the dictionary.json
fieldname_changes = {"ADI_RRB_TOTAL_C": "ADI_R_RRB_TOTAL_C", "ADOS_GOTHAM_SOCAFFECT": "ADOS_GOTHAM_SOC_AFFECT"}

df = pd.read_csv(INPUT, keep_default_na=False)
df.rename(fieldname_changes, axis=1, inplace=True)
df.to_csv(OUTPUT, sep='\t', index=False)
