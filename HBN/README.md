# Child Mind Institute Healthy Brain Network (HBN)

From the [About page of the HBN website](http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/About.html):

> An ongoing initiative focused on creating and sharing a biobank comprised of
> data from 10,000 New York City area children and adolescents (ages 5-21). The
> Healthy Brain Network has adopted a community-referred recruitment model.
> Specifically, study advertisements seek the participation of families who have
> concerns about one or more psychiatric symptoms in their child. The Healthy
> Brain Network Biobank houses data about psychiatric, behavioral, cognitive,
> and lifestyle (e.g., fitness, diet) phenotypes, as well as multimodal brain
> imaging, electroencephalography, digital voice and video recordings, genetics,
> and actigraphy. Beyond accelerating transdiagnostic research, we discuss the
> potential of the Healthy Brain Network Biobank to advance related areas, such
> as biophysical modeling, voice and speech analysis, natural viewing fMRI and
> EEG, and methods optimization.

## Steps to produce this study's data dictionaries

Note: Some of the following COINS access instructions were copied from [the HBN Phenotypic Data Access webpage](http://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/Pheno_Access.html).

1. Go to [the COINS Data Exchange website](https://portal.trendscenter.org/micis/index.php?subsite=dx).
1. Log in using your COINS user ID and password. If you do not have an account, select the **Get Account** option.
1. From the main screen of the COINS Data Exchange, click on **Study Information**.
1. Click on the drop-down for **Select a study** and choose **CMI_HBN**.
1. Under **Study Docs:** download the **all_data_dicts_Aug_2018.zip** into the `HBN/` subfolder without renaming the ZIP file.
1. Unzip the ZIP file in place. The `HBN/` subfolder hierarchy should now look like this:

    ```shell
    HBN/
    ├── all_data_dicts_Aug_2018.zip
    ├── Data Dictionaries/
    ├── dictionary.py
    └── README.md
    ```



1. Install the required Python 3 library with the following line of code:

    ```shell
    python3 -m pip install --user pandas openpyxl
    ```

1. Run the following line of code within the `HBN/` subfolder:

    ```shell
    python3 dictionary.py
    ```

## Notes about this data dictionary

1. Some questionnaires (listed [here](https://github.com/ericearl/dataset-phenotypes/commit/b5c5a79b25e16ec52d5be95e823e7009bb54f437#diff-16cf6d43d5333bdca703a165d985b8db884e7ddb77798e3e377711026f02a6d3R50)) have an entry on the last line that states "Continue
to" which is ignored when creating the corresponding `.json` files for that questionnaires.
1. On some questionnaires the ShortName is entered as `Variable Name` on others as `Variable`
1. Similarly, the `Description` header, which contains the description for every
   question on the questionnaire was entered as `Question`, `Question `, or `Item`
1. Some questionnaires used `Value Labels` instead of `Value Label` to describe
   the range of possible values.
1. Many of the levels from different questionnaire needed adjustments that were
   provided as notes on the `.xlsx` file. The code has many different if
   statements to handle the correct behaviour for each questionnaire.
1. The `SWAN` questionnaire is provided twice with the same data with the name
   `SWAN.xlsx` and `SWAN .xlsx`
1. Some of the levels on `SCARED_P` AND `SCARED_SR` are defined as values that
   are `>=` to a specific threshold
