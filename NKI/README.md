![Brainhack DC Badge](https://img.shields.io/badge/brainhackdc-Capitol%20Cognition-blue?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAA7DAAAOwwHHb6hkAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAdtJREFUOI2tlM9rE1EQx78zb982dd2WDUkbFFGKrXj0IIhePPT/8d/zlpvgwauIoGjRgonubhKSje6++XqQQij5ZcnAHN4wn+8Mw8wTktil6U7VthWcTqe98Xj8cJvcaJskkh3nwlbFtxKs63oMAEmyOXdj1TzPD+I4Po1jfZTn+cFGRZIrvd/vR0VRPLh6V1V1n2S0jpF1azOZTM5IGslDkgFA6ZyL0zT9uIpZO0NV3QMwTJLkGwCX53kG4HAds04wFhEvIr6qqu58PhcRgYh4ADGAP0ubWKVWFEVvMBi8b5omCeH3U+99EkXRXQCfiqLo/XeHzrmX7Xb7p3OUptGpKh4DOFXVrnPOA7hYxklZlieqenwt/oLkXJUDkrcB1yX51TnZM4MnmQL4JSKfAYQryMx+RCRDmqZvF9Umk0lHRBgCL83YtFpRHkI4CcEuncNzsn5t5s/TNH2zyJVleU/5b29s0c3sFoBCRLyqHtd1fYdkW0SU1HdknIlIcp0jyaUzFJFRCGEmIh1VrYDmSES9962mrutzMwuq+mEpOxwOU+dcthjc31dXVRZEJPPeH4UQvqjqEzNrAQhm9l1ELsysWeSyLMvXnt4196PR6NVsNnp249O7ie38x/4LeGtOsdcfsLwAAAAASUVORK5CYII=)

# (work in progress) Enhanced Nathan Kline Institute - Rockland Sample

From the [Enhanced Nathan Kline Institute - Rockland Sample website](https://www.humanconnectome.org/study/hcp-young-adult/document/1200-subjects-data-release):

> The enhanced Nathan Kline Institute-Rockland Sample (NKI-RS) is an ongoing,
> institutionally centered endeavor aimed at creating a large-scale (N > 1000)
> community sample of participants across the lifespan. Measures include a wide
> array of physiological and psychological assessments, genetic information,
> and advanced neuroimaging. Anonymized data will be publicly shared openly and
> prospectively (i.e., on a quarterly basis).

## Steps to produce this study's data dictionaries

1. Make sure you have MATLAB installed (this code was written using R2022b).
1. [Download the zip of the Assessment Documentation](https://fcon_1000.projects.nitrc.org/indi/enhanced/documentation.html) without renaming the ZIP file.
1. Unzip the `assessments_documentation.zip` into the `NKI/` subfolder. It should produce a subfolder named `assessments_documentation/`.
1. Run the `make_dictionaries.m` script as a MATLAB script from within this folder.

## Notes

- This work in progress is not yet complete and will produce non-BIDS-valid JSON data dictionaries of the format:

    ```json
    "ACDS_01": {
        "QuestionLabel": "CARELESS/SLOPPY",
        "QuestionDescription": "Childhood ADHD Symptoms: Prior to Age 7",
        "ResponseLabel": [
            "NO",
            "YES",
            "Don't Know",
            "Missing Data"
        ],
        "ResponseValue": [
            0,
            1,
            null,
            null
        ]
    },
    ```

- JSONs will output into a `phenotype/` subdirectory.
- A Python code refactoring plan is in Issue [#22](https://github.com/ericearl/dataset-phenotypes/issues/22).
