# Philadelphia Neurodevelopmental Cohort (PNC)

From the [Database of Genotypes and Phenotypes (dbGaP) page on Neurodevelopmental Genomics: Trajectories of Complex Phenotypes](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000607.v3.p2):

> This study is a collaboration between the Center for Applied Genomics (CAG) at
> Children's Hospital of Philadelphia (CHOP) and the Brain Behavior Laboratory
> at the University of Pennsylvania (Penn). The cohort consists of youths aged
> 8-21 years who consulted the CHOP network and volunteered to participate in
> genomic studies of complex pediatric disorders. All participants underwent
> clinical assessment, including a neuropsychiatric structured interview and
> review of electronic medical records. They were also administered a
> neuroscience based computerized neurocognitive battery (CNB) and a subsample
> underwent neuroimaging.

## Steps to produce this study's data dictionary

1. Install the required Python 3 library with the following line of code:

    ```shell
    python3 -m pip install --user xmltodict
    ```

1. Go to the [dbGaP Study Accession: phs000607.v3.p2 webpage](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000607.v3.p2&pht=3445).
1. Click the **Phenotype Datasets** tab.
1. Under **Dataset Summary** section below, click on the **Download Data Dictionary** link and save the file to the `PNC/` subfolder by either:
    - Right-clicking and downloading the XML file. ; OR
    - Left-clicking to follow opening the XML file into its own page and then saving the XML file.
1. Do not rename the XML file from its originally downloaded name.
1. Run the following line of code within the `PNC/` subfolder:

    ```shell
    python3 dictionary.py
    ```

## Notes about this data dictionary

The BIDS `LongName` in this dictionary is the `description` from the XML.
The BIDS `Description` is either of:

- `type` from the XML ; OR
- `type` and `comment` from the XML separated by a comma and a space, when a `comment` is present.

`Units` have been added as-is from the XML's `unit` field.

## Steps to produce this study's tabular data

1. Go to the [dbGaP Study Accession: phs000607.v3.p2 webpage](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000607.v3.p2).
1. At the top, just under the **dbGaP Study Accession: phs000607.v3.p2** heading, click on the **Request Access** button which should take you to [the dbGaP authored access portal](https://dbgap.ncbi.nlm.nih.gov/aa/wga.cgi?login=&page=login).
1. Click the **Log In to dbGaP** link toward the top of the content in the page.
1. Fill out any missing required information.
1. On the **My Research Projects** page, there should be...
