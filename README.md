# Pyramid Learning Journal

**Author**: Megan Flood

**Version**: 3.0.0

## Overview
Blog created with Pyramid for recording a Learning Journal of Code 401: Python

Deployed on Heroku: https://mus-learning-journal.herokuapp.com/

## Routes
- `/` - the home page with a listing of all entries
- `/journal/{id:\d+}` - the page for an individual entry
- `/journal/{id:\d+}/edit-entry` - edit an existing entry
- `/journal/new-entry` - add a new entry to the journal

## Getting Started
- Clone this repository to your local machine.

- Once downloaded, `cd` into the `pyramid-learning-journal` directory.

- Begin a new virtual environment with Python 3 and activate it.

- Install and start the server with:

```bash
$ pip install -e .[testing]
$ pserve development.ini --reload
```

- Application is served on http://localhost:6543

## Architecture
Written in Python, with pytest and tox for testing. Uses the web framework Pyramid with a scaffold built with the Cookiecutter pyramid-cookiecutter-alchemy. Database run through PostgresSQL using psycopg2 and SQLAlchemy. Deployed with Heroku.

All tests passing in Python 2 and 3.

## Contributors
[Michael Shinners](https://github.com/mshinners) - Help building out the site using Pyramid

## Change Log
**11-4-2017 3:04pm** - Made learning journal entries into Models connected to a database. View has 100% coverage on Python 2 and 3.

**11-3-2017 6:19pm** - Templating for all pages using Jinja2, pages are now dynamically filled. View has 100% coverage on Python 2 and 3.

**10-31-2017 10:25pm** - All pages are static, but successfully deployed to Heroku. View has 100% coverage on Python 2 and 3.

