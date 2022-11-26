# UK Biobank

From the [UK Biobank "About Us" page](https://www.ukbiobank.ac.uk/learn-more-about-uk-biobank/about-us):

> UK Biobank is a large-scale biomedical database and research resource,
> containing in-depth genetic and health information from half a million UK
> participants. The database, which is regularly augmented with additional
> data, is globally accessible to approved researchers and scientists
> undertaking vital research into the most common and life-threatening
> diseases. UK Biobank’s research resource is a major contributor to the
> advancement of modern medicine and treatment and has enabled several
> scientific discoveries that improve human health.

## Steps to produce this data dictionary

1. Go to the [UK Biobank data access guide page](https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=AccessingData).
2. Click the **Download data dictionary - tsv format** link and place the download into the `UKB/` subfolder.
3. Do not rename the above file from its originally downloaded name.
4. Go to [the MRCIEU/PHESANT repository's release "v1.1" on GitHub](https://github.com/MRCIEU/PHESANT/releases/tag/v1.1)
5. Download the **Source code (zip)** asset and unzip the `PHESANT-1.1.zip` into the `UKB/` subfolder so it looks like this:

    ```shell
    UKB/
    ├── Data_Dictionary_Showcase.tsv
    ├── dictionary.py
    ├── PHESANT-1.1/
    │   ├── biobank-PHESANT-figure.pdf
    │   ├── LICENCE
    │   ├── PHESANT-counter-codes.pdf
    │   ├── PHESANT-logging-information.md
    │   ├── PHESANT-viz/
    │   ├── README.md
    │   ├── resultsProcessing/
    │   ├── testWAS/
    │   ├── ukb_data_codes/
    │   ├── variable-info/
    │   └── WAS/
    └── README.md
    ```

6. Run the following line of code within the `UKB/` subfolder:

    ```shell
    python dictionary.py
    ```

## Notes about this data dictionary

The BIDS `LongName` is composed of the pipe-separated (a pipe is this `|` character) list of the `path` and `category` to uniquely identify each.
`ValueType` has been inserted directly from the **Data_Dictionary_Showcase.tsv** and is not actually a normal BIDS sidecar metadata JSON field.
`Units` have been added as-is from the **Data_Dictionary_Showcase.tsv**.
This design choice was to save time from having to find each individual BIDS-proper unit.
