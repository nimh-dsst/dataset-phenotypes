#! /usr/bin/env python3


# imports
import json
import xmltodict
import xml.etree.ElementTree as ET
from pathlib import Path


# file path handling
HERE = Path(__file__).parent.resolve()
INPUT = HERE.joinpath('phs000607.v3.pht003445.v3.Neurodevelopmental_Genomics_Subject_Phenotypes.dictionary.xml')
OUTPUT = HERE.joinpath('phenotype', 'phenotype.json')
status = OUTPUT.parent.mkdir(parents=True, exist_ok=True)


# read in the data dictionary
with open(INPUT, 'r') as f:
    xmltxt = f.read()

# parse the XML
xd = xmltodict.parse(xmltxt)
dt = xd['data_table']
entries = dt['variable']

# create an output dictionary
dictionary = {}

# write a file for the output data dictionary JSON
with open(OUTPUT,'w') as f:

    # loop over the entries
    for entry in entries:

        # parse the name/description/type/value, but skip the entry on failure
        try:
            ename = entry['name']
        except:
            continue

        try:
            edesc = entry['description']
        except:
            continue

        try:
            etype = entry['type']
        except:
            continue

        try:
            evalues = entry['value']
        except:
            continue

        # parse comment and unit, but set to None on failure
        try:
            ecomm = entry['comment']
        except:
            ecomm = None

        try:
            eunit = entry['unit']
        except:
            eunit = None

        levels = {}

        # loop over the values if more than one
        if len(evalues) > 1:
            for i, evalue in enumerate(evalues):

                # if it's a dictionary instance, parse the key and value
                if isinstance(evalue, dict):
                    levels[evalue['@code']] = evalue['#text']

                # if the length is 2
                elif len(evalues) == 2:
                    levels[evalues['@code']] = evalues['#text']
                    # stop after the first one
                    break
                
                # otherwise, print a debugging message
                else:
                    print(ename, str(i) + ': ', evalue)

        # fill in the output dictionary
        dictionary[ename] = {}
        dictionary[ename]["LongName"] = edesc

        if ecomm:
            dictionary[ename]["Description"] = etype + ", " + ecomm
        else:
            dictionary[ename]["Description"] = etype

        dictionary[ename]["Levels"] = levels

        if eunit:
            dictionary[ename]["Units"] = eunit

    # write the output dictionary to the JSON file
    f.write(json.dumps(dictionary, indent=4))
