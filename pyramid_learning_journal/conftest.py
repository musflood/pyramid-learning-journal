"""Fixtures for the pyramid_learning_journal tests."""

from __future__ import unicode_literals
from pyramid import testing
from pyramid_learning_journal.models.meta import Base
from pyramid_learning_journal.models import Entry, get_tm_session
import transaction
import os
import pytest


@pytest.fixture
def test_entry():
    """Create a new Entry."""
    return Entry(
        title='test entry',
        body='This is a test.'
    )


@pytest.fixture(scope='session')
def configuration(request):
    """Setup a database for testing purposes."""
    config = testing.setUp(settings={
        'sqlalchemy.url': os.environ['TEST_DATABASE_URL']
    })
    config.include('pyramid_learning_journal.models')
    config.include("pyramid_learning_journal.routes")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a database session for interacting with the test database."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy GET request with a dbsession."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_entry(dummy_request, test_entry):
    """Create a new Entry and add to database."""
    dummy_request.dbsession.add(test_entry)
    return test_entry


@pytest.fixture
def add_entries(dummy_request, test_entries):
    """Create a new Entry and add to database."""
    dummy_request.dbsession.add_all(test_entries)
    return test_entries


@pytest.fixture(scope="session")
def testapp(request):
    """Functional test for app."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        settings = {
            'sqlalchemy.url': os.environ['TEST_DATABASE_URL']
        }
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('pyramid_learning_journal.routes')
        config.include('pyramid_learning_journal.models')
        config.scan()
        return config.make_wsgi_app()

    app = main()

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tearDown)

    return TestApp(app)


@pytest.fixture(scope='session')
def test_entries():
    """Create a list of Entry objects to be added to the database."""
    return [
        Entry(
            title='Day {}'.format(i),
            body='words ' * (i + 1)
        ) for i in range(20)
    ]


@pytest.fixture(scope='session')
def fill_the_db(testapp, test_entries):
    """Fill the test database with dummy entries."""
    SessionFactory = testapp.app.registry['dbsession_factory']
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(test_entries)
