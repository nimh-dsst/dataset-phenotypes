# Adolescent Brain Cognitive Development Study (ABCD)

From the [ABCD Study's "About" webpage](https://abcdstudy.org/about/):

> The Adolescent Brain Cognitive Development (ABCD) Study® is the largest
> long-term study of brain development and child health in the United States.
> The National Institutes of Health (NIH) funded leading researchers in the
> fields of adolescent development and neuroscience to conduct this ambitious
> project. The ABCD Research Consortium consists of a Coordinating Center, a
> Data Analysis, Informatics & Resource Center, and 21 research sites across the
> country (see map), which have invited 11,880 children ages 9-10 to join the
> study. Researchers will track their biological and behavioral development
> through adolescence into young adulthood.

## Steps already done to produce the preliminary data dictionaries saved here

1. Went to the [NIMH Data Archive (NDA) website](https://nda.nih.gov/).
1. Downloaded all the NDA's ABCD Release 4.0 Tabulated Data structure definitions to the `nda_data_structure_definitions` subfolder.
1. Committed them into version control here.
1. "Manually" edited some of the NDA data structure definition CSVs, as necessary, to match the intent of each question.
1. Committed the edits into version control here.

## Steps to produce this study's data dictionaries

1. Install the required Python 3 library with the following line of code:

    ```shell
    python3 -m pip install --user pandas
    ```

1. Run the following line of code within the `ABCD/` subfolder:

    ```shell
    python3 dictionary.py
    ```

1. Note: Many print statements will pop up, but these have all been reviewed manually and addressed programmatically, as necessary, in parts of the `dictionary.py` script.

## Notes about these data dictionaries

1. Though `DataType` is not a BIDS-valid field in the sidecar JSON, it has been included for reference.
1. Likewise `ValueRange` has been included though it is not BIDS-valid.
1. The `Description` is also pipe-separated (this `|` character) with the `Notes`, when `Notes` are present.
