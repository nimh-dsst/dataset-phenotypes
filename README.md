# "Big" Neuroimaging Dataset Phenotype BIDS Tools

Preparatory scripts to output BIDS phenotypic data dictionaries and transform phenotypic data to BIDS TSVs for common neuroimaging datasets.

These tools follow the guidelines of [BIDS Extension Proposal 36 (BEP036)](https://docs.google.com/document/d/1WTkfES8L0vItZVyyR68fc-9cO03jS-kCnMnw6602pbc/edit#heading=h.gjdgxs). The hope is for researchers to embrace this BIDS Phenotypic Data standard, by seeing examples in their favorite datasets.

## Washington DC - Brainhack 2022

### Project Description

Information about phenotypes (i.e., age, responses to cognitive/clinical questionnaires, blood tests) is hard to share and varies widely in format when shared. For example, some studies share this information in `.tsv`, `.csv`, and some even share this information in `.pdf` or Excel files. Building upon the recent [guidelines for phenotypic data in BIDS](https://docs.google.com/document/d/1WTkfES8L0vItZVyyR68fc-9cO03jS-kCnMnw6602pbc/edit#heading=h.4k1noo90gelw), we created a repository to share the phenotypes in a uniform & machine-readable format for a few commonly used neuroimaging datasets.
We have written the code to extract a dictionary.json (a file that contains a list of the phenotypes present and their description) for a few datasets, but this can be extended to other neuroimaging datasets. A list of other possible contributions is present on the [github issues](https://github.com/ericearl/dataset-phenotypes/issues).

## Dataset requests

Do you not see your favorite neuroimaging dataset's phenotypic data here? Add a GitHub Issue describing how to download the phenotypic data dictionaries and the phenotypic data and the dataset will be added to the queue.

## Contributions

Contributors are always welcome to add GitHub Issues describing any inaccuracies or feature requests. GitHub Pull Requests are also always welcome to initiate a review of some fix or addition to the repository.

## Queue (last updated December 8th, 2022)

1. HBN data dictionaries
1. All studies' phenotypic data BIDS TSV transformation scripts
