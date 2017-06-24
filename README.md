
# wc.py

This repository contains the CLI and SDK for the WordCount Python [ wc.py ] developer tool.

## Overview

This script provides a set of tools to analyse the number of occurences of words across a single or multiple documents. It can be accessed through the CLI, or directly through the SDK provided by the `WCExtractor` class in the `wcpy` module.

For the **CLI interface quickstart** please refer to the **User Guide below**.

For the **SDK interface quickstart** please refer to the **Developer Guide below**.

For more advanced documnetation please refer to the official [WCPY documentation](https://axsauze.github.io/wcpy/).

# Installation

You can install it from pip by running the following:

```
pip install wc.py
```

This will install the script in your computer so you'll be able to call it directly with `wc.py`.

# CLI User Guide

The main user interface of this library is through the command line interface

Some example usages include the following

#### Word occurences in documents in this folder recusively

```
wc.py --paths ./
```

#### Word occurrences in this folder docs with limit of top 10

```
wc.py --paths ./ --limit 10
```

#### Word occurences in specific file filtered on specific words

```
wc.py --paths ./ tests/test_data/doc1.txt --filter-words tool awesome an
```

#### Word occurences in folder with output truncated and only 2 columns

```
wc.py --paths tests/test_data/ --truncate 100 --columns word count
```

#### Saving output to file

```
wc.py --paths ./ --filter-words tool awesome an --truncate 50 --output output.txt
```


# Development

## Install VirtualEnv and Requirements

Python 3.X is used, and it's strongly recommended to set up the project in a virtual environment:

```
virtualenv --no-site-packages -p python3 venv
```

Then install it using the setup.py command

```
python setup.py install_data
```

## NLTK

This package uses the NLTK `english.pickle` dataset. The dataset includes in both, the repository and the PyPi package, however if you want to donwload more of the languages you can do so with the following command:

```
python -c "import nltk; nltk.download('punkt')"
```


# Testing

`py.test` is used to run the tests, in order to run it simply run:

```
python setup.py test
```

# Cleaning

To clean all the files generated during runtime simply run:

```
python setup.py clean
```


