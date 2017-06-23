
# wc.py

WordCount analysis of documents in Python.

## Overview

This script provides a set of tools to analyse the number of occurences of words across a single or multiple documents.

## Installationg

You can install it from pip by running the following:

```
pip install wc.py
```

This will install the script in your computer so you'll be able to call it directly with `wc.py`.

## Usage

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

The previous command must have installed the NLTK dependencies, but if by any reason it's not working for you, you can install it with the following:

```
python -c "import nltk; nltk.download('punkt')"
```

Regardless this project has a fallback on REGEXes in case that the NLTK package fails for any reason.


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


