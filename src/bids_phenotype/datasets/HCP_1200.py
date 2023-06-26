"""
Human Connectome Project tabular phenotype data and dictionary conversion to BIDS TSV and JSON files.
"""


import pandas
import re
from glob import glob
from pathlib import Path


# convert words and strings to exclusively alphanumerics for BIDS' sake
def bidsify(input_name):
    return re.sub(r'[\W_]+', '', input_name)


def data(input, output):
    for tabular_phenotype in [str(list(input.glob('unrestricted_*.csv'))[0]), str(list(input.glob('RESTRICTED_*.csv'))[0])]:
        # file path handling
        INPUT = Path(tabular_phenotype)
        OUTPUT = output.joinpath('phenotype', re.sub(r'_.+', '.tsv', INPUT.name))
        status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)

        df = pandas.read_csv(INPUT, keep_default_na=False, low_memory=False)
        df.insert(0, 'participant_id', df['Subject'].apply(lambda x: 'sub-' + bidsify(str(x))))
        df.to_csv(OUTPUT, sep='\t', index=False)

    return


def dictionary(input, output):
    # imports
    import json
    import os
    import shutil


    # file path handling
    INPUT = input.joinpath('HCP_S1200_DataDictionary_April_20_2018.xlsx')
    OUTPUT = output.joinpath('phenotype', 'unrestricted.json')
    status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)


    # reading in the original data dictionary
    original = pandas.read_excel(INPUT)

    # start with a new/empty data dictionary
    data_dict = {
        "participant_id": {
            "LongName": "Participant Identifier",
            "Description": "Unique BIDS identifier for the participant in this study."
        }
    }

    # begin the output file since the mkdir command above created its directory
    with open(OUTPUT, 'w') as f:
        # loop over the rows of the original data dictionary
        for i in range(original.shape[0]):

            # get the "columnHeader" as the BIDS field/short name
            try:
                ShortName = str(original['columnHeader'][i])
            except:
                # go to next row if columnHeader errors
                continue

            # set the BIDS long name to "category|assessment|fullDisplayName"
            try:
                LongName = '|'.join([ str(original['category'][i]) , str(original['assessment'][i]) , str(original['fullDisplayName'][i]) ])
            except:
                # go to next row if category, assessment, or fullDisplayName error
                continue

            # set the BIDS description to the original "description"
            try:
                Description = str(original['description'][i])
            except:
                # go to next row if description errors
                continue

            # set the BIDS field/short name and insert the long name and description
            data_dict[ShortName] = {}
            data_dict[ShortName]["LongName"] = LongName
            data_dict[ShortName]["Description"] = Description

            # parse the BIDS "Levels" per ShortName, when present
            levels = {}

            # only has levels when "=" is present and we're ignoring "href"
            if '=' in Description and 'href' not in Description:

                # find all the evidence of Levels in the Description
                matches = re.findall('[;:\(\?\.] *.+= *.+', Description)

                # when there's evidence of Levels, parse them out
                if matches:

                    # first match in "phrase" is start index of something with "="
                    phrase = matches[0]

                    # iterate through "phrase" characters
                    for start_idx, char in enumerate(phrase):
                        if ' ' in char or '(' in char:
                            # break to preserve the found character index
                            break

                    # use the found character index to get the "Levels" string
                    start_idx += 1

                    # ignore ending with closed parentheses
                    if phrase[-1] == ')':
                        substring = phrase[start_idx:-1]
                    else:
                        substring = phrase[start_idx:]

                    # skip some phrases that do not need Levels
                    if 'Illumina' not in substring and 'theta' not in substring and 'Zygosity' not in substring and '100%' not in substring and 'Most cigarettes smoked in a day' not in Description:

                        # psecial cases for "Levels" parsing
                        if ShortName == 'SSAGA_Employ':
                            substring_split = substring.replace(';', ',').split(',')
                        elif ShortName == 'Acquisition':
                            substring_split = substring.split('collection.')[1].split(',')
                        elif ShortName == 'SSAGA_TB_Age_1st_Cig':
                            substring_split = substring.split('even a puff), (')[1].split(',')
                        elif ShortName in ['PSQI_Other', 'PSQI_SleepMeds', 'PSQI_DayStayAwake'] or Description.startswith('PSQI 5.'):
                            substring_split = '0=Not during the past month, 1=Less than once a week, 2=Once or twice a week, 3=3 or more times a week'.split(',')
                        elif ShortName == 'PSQI_Quality':
                            substring_split = '0=Very good, 1=Fairly good, 2=Fairly bad, 3=Very bad'.split(',')
                        elif ShortName == 'PSQI_DayEnthusiasm':
                            substring_split = '0=No problem at all, 1=Only a very slight problem, 2=Somewhat of a problem, 3=A very big problem'.split(',')
                        elif ShortName == 'PSQI_BedPtnrRmate':
                            substring_split = '0=No bed partner or roomate; 1=Partner/roomate in other room; 2=Partner in same room, but not same bed; 3=Partner in same bed'.split(';')
                        elif 'NEORAW_' in ShortName:
                            substring_split = 'SA=Strongly Agree, A=Agree, N=Neither Agree or Disagree, D=Disagree, SD=Strongly Disagree'.split(',')
                        elif ';' in substring:
                            substring_split = substring.split(';')
                        else:
                            substring_split = substring.split(', ')
                            if ShortName in ['SSAGA_PanicDisorder', 'SSAGA_Agoraphobia']:
                                del(substring_split[2])

                        # reassign the variable name to something clearer for below
                        level_list = substring_split

                        # skip doing automatically for these two, manual fixes below
                        if ShortName in ['Acquisition', 'SSAGA_Income']:
                            continue

                        # iterate through the "Levels" list
                        for level in level_list:

                            # if there's an "=" in the level, parse both sides
                            if '=' in level:
                                if '>=' in level or '<=' in level or ' = ' in level:
                                    pair = level.split(' = ')
                                else:
                                    pair = level.split('=')

                                # clean up the "Levels" key and value
                                level_key = str(pair[0].lstrip().rstrip().replace(' (Asked of female participants only)','').replace(' (Asked of female participants only',''))
                                level_value = str(pair[1].lstrip().rstrip().replace(' (Asked of female participants only)','').replace(' (Asked of female participants only',''))

                            # if there's no "=", then the level is the key and value
                            else:
                                # clean up the level key
                                level_key = str(level.lstrip().rstrip())

                                # "copy" the key into the value
                                level_value = level_key

                            # pass if the level key is an integer
                            try:
                                level_key_int = int(level_key)
                            except:
                                # pass if the level value is an integer
                                try:
                                    level_value_int = int(level_value)

                                    # swap the key and value if it gets here
                                    temp = level_key
                                    level_key = level_value
                                    level_value = temp

                                # otherwise it's probably a string
                                except:

                                    # skip this erroneous level_key with no value
                                    if level_key == ' etc.':
                                        continue

                                    # some nice debugging warning messages
                                    elif not ('Agree' in level_value or 'Disagree' in level_value or 'if male' in level_value or 'if female' in level_value):
                                        print(f'problem with level: {level}')
                                        print(f'             level_key: {level_key}')
                                        print(f'             level_value: {level_value}')

                            # add the level key and value to the "levels" dictionary
                            levels[level_key] = level_value

            # if the levels dictionary is not empty, add it to the dictionary
            if levels:
                data_dict[ShortName]["Levels"] = levels

        # correct ten "Levels" lists
        data_dict['Acquisition']['Levels'] = {
                "Q1": "8/2012 - 10/2012 (Aug-Oct)",
                "Q2": "11/2012 - 1/2013",
                "Q3": "2/2013 - 4/2013",
                "Q4": "5/2013 - 7/2013",
                "Q5": "8/2013 - 10/2013"
            }
        data_dict['SSAGA_Income']['Levels'] = {
                "1": "<$10,000",
                "2": "10K-19,999",
                "3": "20K-29,999",
                "4": "30K-39,999",
                "5": "40K-49,999",
                "6": "50K-74,999",
                "7": "75K-99,999",
                "8": ">=100,000"
            }
        data_dict['SSAGA_ChildhoodConduct']['Levels'] = {
                "0": "None",
                "1": "1",
                "2": "2, if male; 2 or more, if female",
                "3": "3 or more, if male"
            }
        data_dict['SSAGA_Alc_D4_Dp_Sx']['Levels'] = {
                "0": "0",
                "1": "1",
                "2": "2, if male; 2+, if female",
                "3": "3+, if male"
            }
        data_dict['SSAGA_Alc_12_Frq']['Levels'] = {
                "1": "4-7 days/week, if male",
                "2": "3 days/week, if male; 3-7 days/week, if female",
                "3": "2 days/week",
                "4": "1 day/week",
                "5": "1-3 days month",
                "6": "1-11 days/year",
                "7": "never in past 12 months"
            }
        data_dict['SSAGA_Alc_12_Frq_5plus']['Levels'] = {
                "1": "3+ days/week, if male",
                "2": "1-2 days/week, if male; 1+ days/week, if female",
                "3": "1-3 days/month",
                "4": "1-11 days/year",
                "5": "never"
            }
        data_dict['SSAGA_Alc_12_Frq_Drk']['Levels'] = {
                "1": "1-7 days/week, if male",
                "2": "1-3 days/month, if male; 1+ days/month, if female",
                "3": "1-11 days/year",
                "4": "never"
            }
        data_dict['SSAGA_Alc_12_Max_Drinks']['Levels'] = {
                "1": "1-2",
                "2": "3-4",
                "3": "5-6",
                "4": "7-8",
                "5": "9-10, if male; 9+, if female",
                "6": "11-12, if male",
                "7": "13+, if male"
            }
        data_dict['SSAGA_Alc_Hvy_Max_Drinks']['Levels'] = {
                "1": "<=3",
                "2": "4-6",
                "3": "7-9",
                "4": "10-12",
                "5": "13-15",
                "6": "16-20, if male; 16+, if female",
                "7": "21+, if male"
            }
        data_dict['SSAGA_Times_Used_Illicits']['Levels'] = {
                "0": "never used",
                "1": "1-2 times",
                "2": "3-10 times",
                "3": "11-25 times",
                "4": "26-100 times, if male; >25 times, if female",
                "5": ">100 times, if male"
            }

        # write out the final JSON with pretty printing
        f.write(json.dumps(data_dict, indent=4))

    phenotype_json_copy1 = str(OUTPUT.parent.joinpath('unrestricted.json'))
    phenotype_json_copy2 = str(OUTPUT.parent.joinpath('RESTRICTED.json'))

    rename_status = os.rename(str(OUTPUT), phenotype_json_copy1)
    copy_status = shutil.copyfile(phenotype_json_copy1, phenotype_json_copy2)

    return
