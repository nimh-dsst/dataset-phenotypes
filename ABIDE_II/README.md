# Autism Brain Imaging Data Exchange II (ABIDE II)

From the [ABIDE II webpage](http://fcon_1000.projects.nitrc.org/indi/abide/abide_II.html):

> ABIDE II was established to further promote discovery science on the brain
> connectome in ASD. To date, ABIDE II has aggregated over 1000 additional
> datasets with greater phenotypic characterization, particularly in regard to
> measures of core ASD and associated symptoms. In addition, two collections
> include longitudinal samples of data collected from 38 individuals at two time
> points (1-4 year interval). To date, ABIDE II involves 19 sites - ten charter
> institutions and seven new members - overall donating 1114 datasets from 521
> individuals with ASD and 593 controls (age range: 5-64 years). These data have
> been openly released to the scientific community on June 2016.

## Steps already done to produce the preliminary data dictionary saved here

1. Went to the [ABIDE II webpage](http://fcon_1000.projects.nitrc.org/indi/abide/abide_II.html).
1. Scrolled down to the **ABIDE II Downloads >> Phenotypic data** section
1. Clicked the **ABIDE II Phenotypic Data Legend** link and downloaded the PDF directly to this `ABIDE_II/` subfolder.
1. Did not rename the PDF file from its originally downloaded name.
1. Installed and used the [Tabula software](https://tabula.technology/) to pull the tables out of the PDF pages and save the output as a TSV.
1. "Manually" edited, as necessary, to eliminate multi-line entries and to match each PDF table's intent.
1. Renamed the filename from `tabula-ABIDEII_Data_Legend.tsv` to more simply `ABIDEII_Data_Legend.tsv`.
1. Committed the final `ABIDEII_Data_Legend.tsv` TSV here to Git version control.

## Steps to produce this study's data dictionary

1. Run the following line of code within the `ABIDE_II/` subfolder:

    ```shell
    python3 dictionary.py
    ```

## Notes about this data dictionary
