# Autism Brain Imaging Data Exchange I (ABIDE I)

From the [ABIDE I webpage](http://fcon_1000.projects.nitrc.org/indi/abide/abide_I.html):

> The Autism Brain Imaging Data Exchange I (ABIDE I) represents the first ABIDE
> initiative. Started as a grass roots effort, ABIDE I involved 17 international
> sites, sharing previously collected resting state functional magnetic
> resonance imaging (R-fMRI), anatomical and phenotypic datasets made available
> for data sharing with the broader scientific community. This effort yielded
> 1112 dataset, including 539 from individuals with ASD and 573 from typical
> controls (ages 7-64 years, median 14.7 years across groups). This aggregate
> was released in August 2012.

## Steps already done to produce the preliminary data dictionary saved here

1. Went to the [ABIDE I webpage](http://fcon_1000.projects.nitrc.org/indi/abide/abide_I.html).
1. Scrolled down to the **ABIDE I Downloads** section
1. Clicked the **Phenotypic Data Legend** link and downloaded the PDF directly to this `ABIDE_I/` subfolder.
1. Did not rename the PDF file from its originally downloaded name.
1. Took screenshots of each table within each page of the PDF and named them as `ABIDE_LEGEND_V1.02_PAGE_#.jpg`
1. Installed and used the Optical Character Recognition (OCR) software [Tesseract](https://tesseract-ocr.github.io/tessdoc/) to convert JPEG tables to text in TXT files, like the following.

    ```shell
    tesseract ABIDE_LEGEND_V1.02_PAGE_1.jpg ABIDE_LEGEND_V1.02_PAGE_1
    ```

1. Renamed each TXT file to a TSV file and "manually" edited, as necessary, to match each PDF table's intent using tabs instead of spaces as field separators.
1. Concatenated the two table TSV files into a single TSV file and committed that here to Git version control.

## Steps to produce this study's data dictionary

1. Install the required Python 3 library with the following line of code:

    ```shell
    python3 -m pip install --user pandas
    ```

1. Run the following line of code within the `ABIDE_I/` subfolder:

    ```shell
    python3 dictionary.py
    ```

## Notes about this data dictionary

1. The BIDS `Description` is mostly composed here of the comma-separated list of `VARIABLE TYPE` then `MIN` then `MAX` because the unique combination of these three describes the data in that field well.
1. The entries for `FIQ`, `VIQ`, and `PIQ` were "manually" adjusted to have simplified `Description` and no more `Levels`.
1. The entries for `FIQ_TEST_TYPE`, `VIQ_TEST_TYPE`, and `PIQ_TEST_TYPE` were "manually" adjusted to include better values in each level of the `Levels` and a shorted `Description`.
1. You can review the exact manual fixes toward the bottom of the `dictionary.py` script.


## Steps to convert this study's phenotype data file from CSV to TSV format

1. Log in on [NITRC repository](https://www.nitrc.org/account/login.php). Register for an account, if you don't already have one.
2. Download raw phenotype data from [ABIDE I page](http://www.nitrc.org/frs/downloadlink.php/4912).
3. Run the following line of code within `ABIDE_I/` subfolder with appropriate file paths in place of `<INPUT_FILE>` and `<OUTPUT_DIR>`:
    ```
    python data_convert.py -i <INPUT_FILE> -o <OUTPUT_DIR>
    ```
    **NOTE** <INPUT_FILE> should be the path to file downloaded in step 2. 
    
## Notes about data conversion script
1. The `ADI_RRB_TOTAL_C` field has been renamed to `ADI_R_RRB_TOTAL_C` to match the one in `dictionary.json`.
2. The `ADOS_GOTHAM_SOCAFFECT` field has been renamed to `ADOS_GOTHAM_SOC_AFFECT` to match the one in `dictionary.json`.
