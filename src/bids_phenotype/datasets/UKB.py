"""
UK Biobank tabular phenotype data and dictionary conversion to BIDS TSV and JSON files.
"""


import re
from pathlib import Path


# convert words and strings to exclusively alphanumerics for BIDS' sake
def bidsify(input_name):
    return re.sub(r'[\W_]+', '', input_name)


def data(input, output):

    return


def dictionary(input, output):

    return
