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

## Steps to convert this study's data files

1. Make sure the system you want to download the data to has at least 25 GB of space.
1. Go to [the NIMH Data Archive's (NDA) ABCD Study page](https://nda.nih.gov/general-query.html?q=query=featured-datasets:Adolescent%20Brain%20Cognitive%20Development%20Study%20(ABCD)).
1. Scroll down to the bottom and find the section labeled **Tabulated Datasets and Raw Behavioral Data**.
1. Click the checkbox on the left side of the row labeled **Release 4.0 Tabulated Behavioral, Questionnaire, and Imaging Data - September 2021 (12 GB)**.
1. An **Updating Data Structures...** modal will pop up. Wait for it to disappear.
1. Click the orange **Add to Workspace** button on the bottom right of the page.
1. Click the Filter icon on the right of the page and then click the **Submit to Filter Cart** button in the bottom of that same sidebar.
1. Wait for the Filter Cart in the top right corner to update.
1. Click the **Create Data Package/Add Data to Study** link in the top right corner.
1. Click **Create Data Package** and give it a Package Name that has no spaces or symbols in it.
1. Click the checkbox to the right of **Include associated data files** then click the large **Create Data Package** button in this dialog.
1. It will offer you another modal with a link at the bottom that says "Click here to navigate to the dashboard" and you should click the **here** link.
1. When the **Status** column of your new data package's row says **Ready to Download**, we recommend the Download Manager for downloading your data smoothly.
1. Download the data to your computer.
1. Place the downloaded data in a new subdirectory called `data/` within the `ABCD/` subdirectory of this repository. It should look something like this:

    ```text
    ABCD/data/
    ├── FILLINTHEBLANK.txt
    ├── ...
    └── FILLINTHEBLANK.txt
    ```

1. Run `data_convert.py` to convert the data files in `.txt` format to BIDS `.tsv` format.

    ```shell
    python3 data_convert.py
    ```

## Notes about the data dictionaries

1. Though `DataType` is not a BIDS-valid field in the sidecar JSON, it has been included for reference.
1. Likewise `ValueRange` has been included though it is not BIDS-valid.
1. The `Description` is also pipe-separated (this `|` character) with the `Notes`, when `Notes` are present.
