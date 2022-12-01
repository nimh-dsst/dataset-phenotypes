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
