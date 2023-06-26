"""
bids-phenotype is a command-line tool for the conversion of tabular phenotype
data and dictionaries to BIDS-formatted TSV and JSON files.
"""


# imports
import argparse
import logging
import os
import sys
from logging import debug
from logging import info
from logging import warning
from logging import error
from logging import critical
from pathlib import Path


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# global variables
DATASETS = [
    'ABCD_4',
    'ABIDE_I',
    'ABIDE_II',
    'HBN',
    'HCP_1200',
    'NKI',
    'PNC',
    'UKB'
]


# functions
def existent(path):
    """
    Check if a path exists
    :param path: Path to check
    :return: Existent path as a Path object
    """
    if not Path(path).exists():
        raise argparse.ArgumentTypeError(f"{path} does not exist")
    return Path(path)


def readable(path):
    """
    Check if a path is readable
    :param path: Path to check
    :return: Readable path as a Path object
    """
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(f"{path} is not readable")
    return Path(path)


def writeable(path):
    """
    Check if a path is writeable
    :param path: Path to check
    :return: Writeable path as a Path object
    """
    if not os.access(path, os.W_OK):
        raise argparse.ArgumentTypeError(f"{path} is not writeable")
    return Path(path)


def executable(path):
    """
    Check if a path is executable
    :param path: Path to check
    :return: Executable path as a Path object
    """
    if not os.access(path, os.X_OK):
        raise argparse.ArgumentTypeError(f"{path} is not executable")
    return Path(path)


def available(path):
    """
    Check if a path has a parent and is available to write to
    :param path: Path to check
    :return: Available path as a Path object
    """
    parent = Path(path).parent.resolve()
    if not (parent.exists() and os.access(str(parent), os.W_OK)):
        raise argparse.ArgumentTypeError(f"""{path} is either not writeable or 
                                          the parent directory does not exist""")

    if Path(path).exists():
        return writeable(path)
    else:
        return Path(path)


# command-line interface
def cli():
    parser = argparse.ArgumentParser(prog='bids-phenotype',
                                     description=__doc__)

    parser.add_argument(choices=DATASETS, dest='dataset', metavar='DATASET',
                        help='Data set/study selection, must be one of: ' +
                             ', '.join(DATASETS) + '.')
    parser.add_argument(dest='input', type=existent, metavar='INPUT',
                        help='Input file path.')
    parser.add_argument(dest='output', type=available, metavar='OUTPUT',
                        help='Output file path.')

    parser.add_argument('-t', '--data', '--tsv', dest='data', action='store_true', default=False,
                        help='Convert the data file(s). This option expects all '
                             'data input files to be in the same flat input '
                             'directory.')
    parser.add_argument('-j', '--dict', '--json', dest='dictionary', action='store_true', default=False,
                        help='Convert dictionary file(s). This option expects all '
                             'dictionary input files to be in the same flat input '
                             'directory.')
    parser.add_argument('-a', '--both', '--all', action='store_true', default=False,
                        help='Convert both the dictionary file(s) and data file(s). '
                             'This option expects all data and dictionary input '
                             'files to be in the same input directory.')

    args = parser.parse_args()

    return args


def main():

    args = cli()

    if args.dataset == 'ABCD_4':
        from .datasets.ABCD_4 import dictionary, data
        info('ABCD_4 dictionary conversion will not use the provided INPUT. This program reads from self-contained/corrected data dictionaries.')

    elif args.dataset == 'ABIDE_I':
        from .datasets.ABIDE_I import dictionary, data
        info('ABIDE_I dictionary conversion will not use the provided INPUT. This program reads from a self-contained/corrected data dictionary.')

    elif args.dataset == 'ABIDE_II':
        from .datasets.ABIDE_II import dictionary, data
        info('ABIDE_II dictionary conversion will not use the provided INPUT. This program reads from a self-contained/corrected data dictionary.')

    elif args.dataset == 'HBN':
        from .datasets.HBN import dictionary, data

    elif args.dataset == 'HCP_1200':
        from .datasets.HCP_1200 import dictionary, data

    elif args.dataset == 'NKI':
        from .datasets.NKI import dictionary, data

    elif args.dataset == 'PNC':
        from .datasets.PNC import dictionary, data

    elif args.dataset == 'UKB':
        from .datasets.UKB import dictionary, data

    else:
        raise ValueError(f"{args.dataset} is not a recognized dataset. Check either the DATASETS list or if/elif section in cli.py's main() function.")


    if args.dictionary or args.both:
        dictionary(args.input, args.output)

    if args.data or args.both:
        data(args.input, args.output)

    if not (args.data or args.dictionary or args.both):
        print('No conversion option selected. '
              'Use -t, -j, or -a options to choose the BIDS conversion you would like. '
              'Or use the -h or --help option for usage instructions.')


if __name__ == '__main__':
    main()
