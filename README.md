## Language Detection

[![Python versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-4682B4.svg?longCache=true&style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Build Status](https://travis-ci.com/anasmounsif/Language_Detection.svg?token=7m4zb6JD1gtxhrzEgWkG&branch=master)](https://travis-ci.com/anasmounsif/Language_Detection)

This project deals with *analysing* and *classifying* the GitHub repositories based on the language used for the drafting of the **README**.

### Requirements

```bash
pip3 install six
pip3 install pytest
pip3 install langdetect
```

### Get Started

To use script individually, if you are using MacOS or Linux type:

`python language_detection.py`

#### Tasks

- [x]    Generation of CSV in output which contains the results of the classification and the new paths after the shift.
- [x]    Moving repositories to dedicated folders based on language detection results.
- [x]    Classification of all READMEs inside the repository.
- [x]    Making CSV as input for the script.

#### How does it work

The script takes as input a CSV file that must contain information on the location of the repositories to be analysed:

| Index    | Path                                  |
|:--------:|---------------------------------------|
| 0        |  Absolute path to repository          |
| 1        |  Absolute path to another repository  |
| ...      | ...                                   |

You can give the script the [*name*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L16) of the CSV by using the configuration file.

##### If you don't have the input.csv

The script is able to automatically generate for you an input.csv file starting from the folder where the repositories are cloned, all you have to do is set `input_generator=1` [*here*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L20) and [*supply*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L21) the path where the repositories are.

---

Language Detection uses the library [*langdetect*](https://github.com/Mimino666/langdetect) which implements an improved Naive Bayes classifier through character normalization and application of specific filters, for more details see: [*langdetect slideshare*](https://www.slideshare.net/shuyo/language-detection-library-for-java).

For each repository, all the READMEs present in the structure are analyzed even if they're nested. Assuming that a repository contains many READMEs written in different languages, the script focuses only on one question;

> *"How much English is in the entire repository?"*

This is to avoid saturating the results with countless codes.

The results are then noted in the CSV generated in output:

| Index    | Path                                           | Readme Analyzed | Language Detected | Code   | Percentage | Code   | Percentage |
|:--------:|------------------------------------------------|:---------------:|-------------------|:------:|:----------:|:------:|:----------:|
| 0        |  Absolute path to analyzed repository          |  1              | `English`         | en     | 100%       | //     | //         |
| 1        |  Absolute path to another analyzed repository  |  2              | `Mixed`           | en     | 60%        | others | 40%        |
| 2        |  Absolute path to another one                  |  1              | `Not English `    | others | 100%       | //     | //         |
| ...      | ...                                            |  ...            | ...               | ...    | ...        | ...    | ...        |

You can change the result by changing the [*maximum*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L37) and [*minimum*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L35) English percentages so that a repository can be classified as:

-   Mixed
-   English
-   Not English

The repositories with an absent and empty README, which have less than the minimum [*number*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L10) of characters or with an extension not supported, will be classified as *Unknown*:


| Index    | Path                                           | Readme Analyzed | Language Detected | Code   | Percentage | Code   | Percentage |
|:--------:|------------------------------------------------|:---------------:|-------------------|:------:|:----------:|:------:|:----------:|
| 0        |  Absolute path to analyzed repository          |  1              | `Unknown`         | //     | //         | //     | //         |
| 0        |  Absolute path to another analyzed repository  |  0              | `Unknown`         | //     | //         | //     | //         |
| ...      | ...                                            | ...             | ...               | ...    | ...        | ...    | ...        |

It will then be up to the user to analyse them manually.

Extensions supported:
-   .markdown
-   .mdown
-   .mdwn
-   .mkdn
-   .mkd
-   .md
-   .txt

GitHub :octocat: provides several *markdowns* that could affect language detection, so the script has an additional feature, that is to **clean** the README analysed by the following markdowns:

-   URLs
-   HTML
-   Links
-   Tables
-   Images
-   Code Snippets
-   Special characters

By default *langdetect* uses a **nondeterministic** approach, this feature is part of the original Google project, if you need to force the algorithm to use a deterministic approach make `translation_type=0` [*here*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L8).

It is also possible to choose where to move the classified repositories:

```
[destinations]
destination_not_english = path
destination_english = path
destination_unknown = path
destination_mixed = path
```

As well as [*disable*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L6) this feature making `moving_feature=0`, or [*disable*](https://github.com/anasmounsif/Language_Detection/blob/master/config.ini#L14) the generation of CSV file in output making `activate_csv_output=0`

If used individually, *it would be appropriate to carefully modify the parameters in the configuration file*.

During the execution the script generates a log file where it is possible to consult all the operations performed as well as the results of the detection.
By default the level is set to INFO, if you need a more detailed logging change this [*line*](https://github.com/anasmounsif/Language_Detection/blob/master/log.conf#L23) to `level=DEBUG` in the configuration file.

:warning: **For the execution to be successful the repositories must be cloned!** :warning:

#### Test

To run the tests, type: `pytest -v` inside the root folder or you can also run specific tests by typing:

`py.test -k <test_name>`

For more information, see the [*documentation*](https://docs.pytest.org/en/stable/contents.html).

### Conclusions

Language Detection is an *integral* part of [*G-Repo*](https://github.com/MatHeartGaming/G-Repo)  project and it was developed in collaboration with the University of Basilicata :top:

---
[![MIT license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/anasmounsif/Language_Detection/blob/master/LICENSE)
