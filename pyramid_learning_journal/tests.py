"""Unit tests basic response test for all view functions."""

from __future__ import unicode_literals
from pyramid.exceptions import HTTPNotFound
from pyramid import testing
from pyramid_learning_journal.models.meta import Base
from pyramid_learning_journal.models import Entry, get_tm_session
import transaction
import pytest


@pytest.fixture(scope='session')
def configuration(request):
    """Setup a database for testing purposes."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://localhost:5432/test-learning-journal'
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
def test_entry(dummy_request):
    """Create a new Entry."""
    new_entry = Entry(
        title='test entry',
        body='This is a test.'
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    return new_entry


def test_list_entries_returns_list_of_entries(dummy_request):
    """Test that the list view function returns a list of the entries."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert 'entries' in response
    assert isinstance(response['entries'], list)


def test_list_entries_returns_all_entries_in_list(dummy_request, test_entry):
    """Test that the list view function returns all entries."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert test_entry.to_html_dict() in response['entries']


def test_detail_entry_returns_one_entry_detail(dummy_request, test_entry):
    """Test that the detail view function returns the data of one entry."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert test_entry.to_html_dict() == response['entry']


def test_error_handling_in_detail_view(dummy_request, test_entry):
    """Test that the on HTTPNotFound is raised if not found."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_create_entry_returns_a_only_the_page_title(dummy_request):
    """Test that the new entry function returns only page title."""
    from pyramid_learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert 'page_title' in response
    assert 'New Entry' == response['page_title']


def test_update_view_returns_only_one_entry_detail(dummy_request, test_entry):
    """Test that the Update view function returns one entry by id."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert test_entry.to_dict() == response['entry']


def test_error_handling_in_update_view(dummy_request, test_entry):
    """Test that the on HTTPNotFound is raised if not found."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


@pytest.fixture(scope="session")
def testapp(request):
    """Functional test for app."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        settings = {
            'sqlalchemy.url': 'postgres://localhost:5432/test-learning-journal'
        }
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include('.models')
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
def fill_the_db(testapp):
    """Fill the test database with dummy entries."""
    SessionFactory = testapp.app.registry['dbsession_factory']
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(ENTRIES)

ENTRIES = [Entry(title='Day {}'.format(i), body='words ' * (i + 1)) for i in range(20)]


def test_home_route_has_all_journal_entries(testapp, fill_the_db):
    """Test that the home route all journal entries."""
    response = testapp.get("/")
    assert len(ENTRIES) == len(response.html.find_all('div', 'card'))


def test_deatil_route_has_one_entry(testapp):
    """Test that the detail_view shows one journal entry."""
    response = testapp.get("/journal/1")
    assert len(response.html.find_all('div', 'card')) == 1
    assert 'Day 0' in response.text


def test_create_view_has_a_create_button(testapp):
    """Test that the Create page has a 'Create' button."""
    response = testapp.get("/journal/new-entry")
    assert len(response.html.find_all('button', attrs={"type": "submit"})) == 1
    assert "Create" in response.html.find('button', attrs={"type": "submit"})


def test_update_view_has_an_update_button(testapp):
    """Test that the Update page has a 'Update' button."""
    response = testapp.get("/journal/1/edit-entry")
    assert len(response.html.find_all('button', attrs={"type": "submit"})) == 1
    assert "Update" in response.html.find('button', attrs={"type": "submit"})
