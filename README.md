# Pyramid Learning Journal

**Author**: Megan Flood

**Version**: 4.0.0

**Deployment Link**: https://mus-learning-journal.herokuapp.com/

## Overview
Blog created with Pyramid for recording a Learning Journal of Code 401: Python

## Architecture
Written in [Python](https://www.python.org/), with [pytest](https://docs.pytest.org/en/latest/) and [tox](https://tox.readthedocs.io/en/latest/) for testing. Uses the web framework [Pyramid](https://trypyramid.com/) with a scaffold built with the Cookiecutter [pyramid-cookiecutter-alchemy](https://github.com/Pylons/pyramid-cookiecutter-alchemy). Database run through [PostgresSQL](https://www.postgresql.org/) using [psycopg2](http://initd.org/psycopg/) and [SQLAlchemy](http://www.sqlalchemy.org/). Deployed with [Heroku](https://www.heroku.com/home).

All tests passing in Python 2 and 3.

## Routes
| Route | Name | Description |
|:--|--|:--|
| `/` | home | the home page with a listing of all entries |
| `/journal/{id:\d+}` | detail | the page for an individual entry by id |
| `/journal/{id:\d+}/edit-entry` | edit | edit an existing entry by id |
| `/journal/{id:\d+}/delete-entry` | delete | delete an existing entry by id |
| `/journal/new-entry` | create | add a new entry to the journal |
| `/login` | login | login to the journal |
| `/logout` | logout | logout from the journal |

## Getting Started

Clone this repository to your local machine.
```
$ git clone https://github.com/musflood/pyramid-learning-journal.git
```

Once downloaded, change directory into the `pyramid-learning-journal` directory.
```
$ cd pyramid-learning-journal
```

Begin a new virtual environment with Python 3 and activate it.
```
pyramid-learning-journal $ python3 -m venv ENV
pyramid-learning-journal $ source ENV/bin/activate
```

Install the application with [`pip`](https://pip.pypa.io/en/stable/installing/).
```
(ENV) pyramid-learning-journal $ pip install -e .[testing]
```

Create a [Postgres](https://wiki.postgresql.org/wiki/Detailed_installation_guides) database for use with this application.
```
(ENV) pyramid-learning-journal $ createdb learning-journal
```

Export environmental variables pointing to the location of database, your username, hashed password, and secret
```
(ENV) pyramid-learning-journal $ export DATABASE_URL='postgres://(your url here)/learning-journal'
(ENV) pyramid-learning-journal $ export AUTH_USERNAME='(username)'
(ENV) pyramid-learning-journal $ export AUTH_PASSWORD='(hashed password)'
(ENV) pyramid-learning-journal $ export AUTH_SECRET='(secret)'
```

Then initialize the database with the `initializedb` command, providing the right `.ini` file for the app's configuration.
```
(ENV) pyramid-learning-journal $ initializedb development.ini
```

Once the package is installed and the database is created, start the server with `pserve` and the right `.ini` file.
```
(ENV) pyramid-learning-journal $ pserve development.ini --reload
```

Application is served on http://localhost:6543

## Testing
Make sure you have the `testing` set of dependancies installed.

You can test this application by first creating a testing database, exporting an environmental variable pointing to the location of the database, then running `pytest` in the same directory as the `setup.py` file.
```
(ENV) pyramid-learning-journal $ createdb test-learning-journal
(ENV) pyramid-learning-journal $ export TEST_DATABASE_URL='postgres://(your url here)/test-learning-journal'
(ENV) pyramid-learning-journal $ pytest
```

For testing in both Python 2 and 3, use the `tox` command instead.
```
(ENV) pyramid-learning-journal $ tox
```

## Contributors
[Michael Shinners](https://github.com/mshinners) - Help building out the site using Pyramid

## Change Log

| Date | &emsp;
| :--- | ---
|**11-11-2017 7:49pm** | Added authorization and authentication for creating, updating, and deleting entries.<br><sup>100% coverage on Python 2 and 3.</sup>
|**11-5-2017 5:20pm** | Added functionality to forms to update and create entries.<br><sup>100% coverage on Python 2 and 3.</sup>
|**11-4-2017 3:04pm** | Made learning journal entries into Models connected to a database.<br><sup>View has 100% coverage on Python 2 and 3.</sup>
|**11-3-2017 6:19pm** | Templating for all pages using Jinja2, pages are now dynamically filled.<br><sup>View has 100% coverage on Python 2 and 3.</sup>
|**10-31-2017 10:25pm** | All pages are static, but successfully deployed to Heroku.<br><sup>View has 100% coverage on Python 2 and 3.</sup>

