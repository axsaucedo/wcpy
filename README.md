
# WordCount Python - [ wc.py ]

Utility tool to count the occurrences of words in text using an NLP tokenizer.

## Overview

This repository contains the CLI and SDK for the WordCount Python [ wc.py ].

`wc.py` provides a set of tools to analyse the number of occurences of words across a single or multiple documents. It can be accessed through the CLI, or directly through the SDK provided by the `WCExtractor` and the `WCCore` classes in the `wcpy` module.

For the **CLI interface quickstart** please refer to the **User Guide below**.

For the **SDK interface quickstart** please refer to the **SDK Interface below**.

For more advanced documnetation please refer to the official [WCPY documentation](https://axsauze.github.io/wcpy/).

# Installation

You can install it from pip by running:

```
pip install wc.py
```

This will install the script in your computer so you'll be able to call it directly with `wc.py`.

# CLI User Guide

## Usage

After installing it you can view the usage and options with `wc.py -h`:

```
usage: wc.py [-h] [-v] [--limit LIMIT] [--reverse]
             [--filter-words FILTER_WORDS [FILTER_WORDS ...]]
             [--file-ext FILE_EXT] [--truncate TRUNCATE]
             [--columns COLUMNS [COLUMNS ...]] [--output-file OUTPUT_FILE]
             paths [paths ...]

Count the number of words in the files on a folder

positional arguments:
  paths                 (REQUIRED) Path(s) to folders and/or files to count words from

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --limit LIMIT         (Optional) Limit the number of results that you would like to display.
  --reverse             (Optional) List is sorted in ascending order by default, use this flag to reverse sorting to descending order.
  --filter-words FILTER_WORDS [FILTER_WORDS ...]
                        (Optional) You can get results filtered to only the list of words provided.
  --file-ext FILE_EXT   (Optional) This is the default file extention for the files being used
  --truncate TRUNCATE   (Optional) Output is often quite large, you can truncate the output by passing a number greater than 5
  --columns COLUMNS [COLUMNS ...]
                        (Optional) This argument allows you to choose the columns to be displayed in the output. Options are: word, count, files and sentences.
  --output-file OUTPUT_FILE
                        (Optional) Define an output file to save the output

EXAMPLE USAGE:
                wc.py ./
                wc.py ./ --limit 10
                wc.py doc1.txt doc2.txt --filter-words tool awesome an
                wc.py docs/ tests/ --truncate 100 --columns word count
                wc.py ./ --filter-words tool awesome an --truncate 50 --output output.txt
```

## Examples

#### Counts of word occurences in documents in this folder recusively

```
wc.py ./
```

#### Word occurrences in this folder docs with limit of the top 10

```
wc.py ./ --limit 10
```

#### Word occurences in multiple files showing only specific words

```
wc.py doc2.txt doc1.txt --filter-words tool awesome an
```

#### Word occurences in folder with output truncated and only 2 columns

```
wc.py tests/test_data/ --truncate 20 --columns word count
```

#### Saving output to file

```
wc.py ./ --filter-words tool awesome an --truncate 50 --output output.txt
```

#### Get the current version

```
wc.py -v
```

# SDK Interface

It is possible to interact with the SDK in multiple levels, the two most common usecases will be:

* WCCore class - Interact with filepaths
* WCExtractor class - Interact with files and text

## WCCore class

### generate_wc_dict(self, paths)

This function finds all the files in a given set of paths, and builds a dictionary with the following structure:


### generate_wc_list(self, paths)

This function finds all the files in a given set of paths, and builds a sorted list (by word count) of the following structure


## WCExtractor class

### extract_wc_from_file

This function extracts all the text from a file and builds a wc_dict object

### extract_wc_from_line

This function extracts all the words from a line and adds it to a wc_dict object

## WCExtractorProcessor class

This class does all the processing to convert a WC Dict into a sorted WCList object.

### process_dict_wc_to_list

As function name suggest, this function converts a WCDict object into a sorted WCList object.

## Core WC Types

### WCDict

```
{
    <WORD_1:: STR>: {
        word_count: <WORD_COUNT:: INT>,
        files: {
            <FILE_PATH:: STR>: [
                <LINE_1:: STR>,
                <LINE_2:: STR>,
                …
            ]
        },
        {
            …
        }
    },
    <WORD_2:: STR>: ...
}
```

### WCList

```
[
    {
        "word": <WORD_1:: STR>,

        word_count: <WORD_COUNT:: INT>,
        files: {
            <FILE_PATH:: STR>: [
                <LINE_1:: STR>,
                <LINE_2:: STR>,
                …
            ]
        }
    },
    {
        "word": <WORD_2:: STR>,
        ...

    }
]
```

# Contributing

If you'd like to contribute, feel free to submit a pull request, open bugs/issues and join the discussion.

## Install VirtualEnv and Requirements

Python 3.X is used, and it's strongly recommended to set up the project in a virtual environment:

```
virtualenv --no-site-packages -p python3 venv
```

Then install it using the setup.py command

```
python setup.py install_data
```

You can also install the requirements directly by running

```
python -r requirements.txt
```

## NLTK

This package uses the NLTK `english.pickle` dataset. The dataset includes in both, the repository and the PyPi package, however if you want to donwload more of the languages you can do so with the following command:

```
python -c "import nltk; nltk.download('punkt')"
```

## Testing

`py.test` is used to run the tests, in order to run it simply run:

```
python setup.py test
```

## Cleaning

To clean all the files generated during runtime simply run:

```
python setup.py clean
```

# Roadmap

* Support multiple types of documents



