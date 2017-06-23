
# Dependencies

## Install VirtualEnv and Requirements

Python 3.X is used, and it's strongly recommended to set up the project in a virtual environment:

```
virtualenv --no-site-packages -p python3 venv
```

Then install the requirements as per requirements.txt:

```
pip install -r requirements.txt
```

## NLTK

I am using the NLTK data package, so you need to make sure you install it with the following command:

```
python -c "import nltk; nltk.download('punkt')"
```


# Testing

Py.test is used to run the tests, in order to run it simply run:

```
python setup.py test
```

# Cleaning

To clean all the files generated during runtime simply run:

```
python setup.py clean
```


