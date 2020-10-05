# Aeternae

Django Starter Project featuring the Creative Landing Page and SB Admin

## System Requirements

- Python v3.8
- Mozilla Geckodriver (for functional tests)

## Setup

```console
$ export VIRTUALENVDIR=~/.virtualenvs/aeternae
$ python3.8 -m venv $VIRTUALENVDIR
$ source $VIRTUALENVDIR/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver
```

You can now visit the website at http://localhost:8000/

## Running Tests

```console
$ which geckodriver # make sure that the geckodriver binary is in your PATH
$ python manage.py test # will run the whole test suite
$ python manage.py <directory> # will run the test suite for that particular directory
$ MOZ_HEADLESS=1 python manage.py test # will run Firefox in headless mode
```

## Pre-Commit Hooks

You can optionally use the included [pre-commit](https://pre-commit.com/) framework to automate linting and formatting of your Python code. To
do this, simply run:

```console
$ pre-commit install
```

The next time you try to commit your changes, your Python files will be automatically linted and formatted in accordance
to [flake8](https://pypi.org/project/flake8/) and [autopep8](https://pypi.org/project/autopep8/)

