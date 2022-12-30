# "Big" Neuroimaging Dataset Phenotype BIDS Tools
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Preparatory scripts to output BIDS phenotypic data dictionaries and transform phenotypic data to BIDS TSVs for common neuroimaging datasets.

These tools follow the guidelines of [BIDS Extension Proposal 36 (BEP036)](https://docs.google.com/document/d/1WTkfES8L0vItZVyyR68fc-9cO03jS-kCnMnw6602pbc/edit#heading=h.gjdgxs). The hope is for researchers to embrace this BIDS Phenotypic Data standard, by seeing examples in their favorite datasets.

## Washington DC - Brainhack 2022

### Project Description

Information about phenotypes (i.e., age, responses to cognitive/clinical questionnaires, blood tests) is hard to share and varies widely in format when shared. For example, some studies share this information in `.tsv`, `.csv`, and some even share this information in `.pdf` or Excel files. Building upon the recent [guidelines for phenotypic data in BIDS](https://docs.google.com/document/d/1WTkfES8L0vItZVyyR68fc-9cO03jS-kCnMnw6602pbc/edit#heading=h.4k1noo90gelw), we created a repository to share the phenotypes in a uniform & machine-readable format for a few commonly used neuroimaging datasets.
We have written the code to extract a dictionary.json (a file that contains a list of the phenotypes present and their description) for a few datasets, but this can be extended to other neuroimaging datasets. A list of other possible contributions is present on the [github issues](https://github.com/ericearl/dataset-phenotypes/issues).

### Contributors during the brainhack
|Name | Github user|
|-----|------------|
|Roberto Salamanca-Giron |[RobertoFelipeSG](https://github.com/RobertoFelipeSG)|
|Josh Faskowitz | [faskowit](https://github.com/faskowit) |


## Dataset requests

Do you not see your favorite neuroimaging dataset's phenotypic data here? Add a GitHub Issue describing how to download the phenotypic data dictionaries and the phenotypic data and the dataset will be added to the queue.

## Contributions

Contributors are always welcome to add GitHub Issues describing any inaccuracies or feature requests. GitHub Pull Requests are also always welcome to initiate a review of some fix or addition to the repository.

## Queue (last updated December 9th, 2022)

1. Add the HBN data dictionaries `dictionary.py`
1. Add all present studies' phenotypic data BIDS TSV transformation scripts as `data_convert.py`
1. Draft and create a phenotypic data browsing, filtering, and selection GUI with [PySimpleGUI](https://www.pysimplegui.org/en/latest/)

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/RobertoFelipeSG"><img src="https://avatars.githubusercontent.com/u/38394703?v=4?s=100" width="100px;" alt="RobertoFelipeSG"/><br /><sub><b>RobertoFelipeSG</b></sub></a><br /><a href="#ideas-RobertoFelipeSG" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!