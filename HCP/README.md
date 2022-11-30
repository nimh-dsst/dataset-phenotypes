# Human Connectome Project Young Adult 1200 Subjects Data Release

From the [Human Connectome Project Young Adult 1200 Subjects Data Release page](https://www.humanconnectome.org/study/hcp-young-adult/document/1200-subjects-data-release):

> The 1200 Subjects Release (S1200) includes behavioral and 3T MR imaging data
> from 1206 healthy young adult participants (1113 with structural MR scans)
> collected in 2012-2015. In addition to 3T MR scans, 184 subjects have
> multimodal 7T MRI scan data and 95 subjects also have some resting-state MEG
> (rMEG) and/or task MEG (tMEG) data available. For the first time, 3T MRI and
> behavioral retest data for 46 subjects is also available.

## Steps to produce this study's data dictionary

1. Install the required Python 3 library with the following line of code:

    ```shell
    python3 -m pip install --user pandas
    ```

1. [Download the "Excel version" of the data dictionary](https://wiki.humanconnectome.org/display/PublicData/HCP-YA+Data+Dictionary-+Updated+for+the+1200+Subject+Release) into the `HCP/` subfolder.
1. Run the following line of code within the `HCP/` subfolder:

    ```shell
    python3 dictionary.py
    ```

## Notes about this data dictionary

The BIDS "LongName" is composed of the pipe-separated (a pipe is this `|` character) list of `category` then `assessment` then `fullDisplayName` because the unique combination of these three seem to create an accurate representation describing the short version of each field.
You may also notice some manual fixes toward the bottom of the `dictionary.py` script to a few fields' `Levels`:

1. Acquisition
1. SSAGA_Income
1. SSAGA_ChildhoodConduct
1. SSAGA_Alc_D4_Dp_Sx
1. SSAGA_Alc_12_Frq
1. SSAGA_Alc_12_Frq_5plus
1. SSAGA_Alc_12_Frq_Drk
1. SSAGA_Alc_12_Max_Drinks
1. SSAGA_Alc_Hvy_Max_Drinks
1. SSAGA_Times_Used_Illicits

These corrections are due to the complex patterns within the levels of the original data dictionary which were easier to instead "inject".
