# Human Connectome Project Young Adult 1200 Subjects Data Release

From the [Human Connectome Project Young Adult 1200 Subjects Data Release page](https://www.humanconnectome.org/study/hcp-young-adult/document/1200-subjects-data-release):

> The 1200 Subjects Release (S1200) includes behavioral and 3T MR imaging data
> from 1206 healthy young adult participants (1113 with structural MR scans)
> collected in 2012-2015. In addition to 3T MR scans, 184 subjects have
> multimodal 7T MRI scan data and 95 subjects also have some resting-state MEG
> (rMEG) and/or task MEG (tMEG) data available. For the first time, 3T MRI and
> behavioral retest data for 46 subjects is also available.

## Steps to produce this study's data dictionary

1. Install the required Python 3 libraries with the following line of code:

    ```shell
    python3 -m pip install --user pandas openpyxl
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

## Steps to produce this study's tabular data

There are two sets, the "Unrestricted" (Open Access) and the "Restricted" datasets. Below are instructions for either separately and then after the same final steps to produce BIDS tabular TSV data.

### For the HCP "Unrestricted" Data

1. Request access to the HCP unrestricted data on ConnectomeDB by **FILL IN THE BLANK**.
1. After approval, login and go to **WU-Minn HCP Data - 1200 Subjects** and click on the Open Dataset button there.
1. It should open to the **HCP 1200 Subject Release "Open Access"** dataset and below in the **Resources** tab and on the left under **Quick Downloads** you can find and click **Behavioral Data** to get the "unrestricted" behavioral data.
1. Save (without renaming) the `unrestricted_[your username]_[datetime of download].csv` to this `HCP/` subfolder. The script will expect the "as-is" original downloaded name of the CSV.

### For the HCP "Restricted" Data

1. Request access for a Principal Investigator (PI) to the HCP restricted data on ConnectomeDB by filling out the **HCP Restricted Data Terms of Use** form indicating you are the PI.
1. Request access for yourself (if you are not the PI) to the HCP restricted data on ConnectomeDB by filling out the **HCP Restricted Data Terms of Use** form for yourself, but referencing your PI.
1. After approval, login and go to **WU-Minn HCP Data - 1200 Subjects** and click on the Open Dataset button there.
1. It should open to the **HCP 1200 Subject Release "Open Access"** dataset. This information can be seen on the top-left corner of the screen.
1. Access the restricted data by clicking where it says **"Open Access"** and choosing **"Restricted (1)"**
1. Now below in the **Resources** tab and on the left under **Quick Downloads** you can find and click **Restricted Data** to get the full "restricted" behavioral dataset.
1. Save (without renaming) the `RESTRICTED_[your username]_[datetime of download].csv` to this `HCP/` subfolder. The script will expect the "as-is" original downloaded name of the CSV.

### Use these same final steps either way

1. If you have not yet, Install the required Python 3 library with the following line of code:

    ```shell
    python3 -m pip install --user pandas
    ```

1. Run the following line of code within the `HCP/` subfolder:

    ```shell
    python3 data.py
    ```

## Notes about this tabular data

1. Things.
1. Stuff.
