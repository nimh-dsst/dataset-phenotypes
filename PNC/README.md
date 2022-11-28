# Philadelphia Neurodevelopment Cohort

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

## Steps to produce this data dictionary

1. Install the required Python 3 library with the following line of code:

    ```shell
    python3 -m pip install --user xmltodict
    ```

2. Go to the [dbGaP Study Accession: phs000607.v3.p2 webpage](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000607.v3.p2&pht=3445).
3. Click the **Phenotype Datasets** tab.
4. Under **Dataset Summary** section below, click on the **Download Data Dictionary** link and save the file to the `PNC/` subfolder by either:
    - Right-clicking and downloading the XML file. ; OR
    - Left-clicking to follow opening the XML file into its own page and then saving the XML file.
5. Do not rename the XML file from its originally downloaded name.
6. Run the following line of code within the `PNC/` subfolder:

    ```shell
    python3 dictionary.py
    ```

## Notes about this data dictionary

The BIDS `LongName` in this dictionary is the `description` from the XML.
The BIDS `Description` is either of:

- `type` from the XML ; OR
- `type` and `comment` from the XML separated by a comma and a space, when a `comment` is present.

`LogicalMin` and `LogicalMax` have been inserted directly from the XML and are not actually normal BIDS sidecar metadata JSON fields.
When present, they are the range of possible values for the field.
`Units` have been added as-is from the XML's `unit` field.
