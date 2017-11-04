"""Unit tests basic response test for all view functions."""

from pyramid.exceptions import HTTPNotFound
from pyramid import testing
from pyramid_learning_journal.models.meta import Base
from pyramid_learning_journal.models import Entry
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


def test_list_entries_returns_list_of_entries(dummy_request):
    """Test that the list view function returns a list of the entries."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert 'entries' in response
    assert isinstance(response['entries'], list)


def test_list_entries_returns_all_entries_in_list(dummy_request):
    """Test that the list view function returns all entries."""
    from pyramid_learning_journal.views.default import list_view
    new_entry = Entry(
        title='test entry',
        body='This is a test.'
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    response = list_view(dummy_request)
    assert new_entry.to_html_dict() in response['entries']


def test_detail_entry_returns_one_detail_entry_in_dict(dummy_request):
    """Test that the detail view function returns the data of one entry."""
    from pyramid_learning_journal.views.default import detail_view
    new_entry = Entry(
        title='test entry',
        body='This is a test.'
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert new_entry.to_html_dict() == response['entry']


def test_error_handling_in_detail_view(dummy_request):
    """Test that the on HTTPNotFound is raised if not found."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_create_entry_returns_a_response_for_new_entry(dummy_request):
    """Test that the new entry function returns a value from a new item."""
    from pyramid_learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert 'page_title' in response
    assert 'New Entry' == response['page_title']


def test_update_view_returns_list_of_entries_in_dict(dummy_request):
    """Test that the Update view function returns a key in the dict."""
    from pyramid_learning_journal.views.default import update_view
    new_entry = Entry(
        title='test entry',
        body='This is a test.'
    )
    dummy_request.dbsession.add(new_entry)
    dummy_request.dbsession.commit()
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert new_entry.to_dict() == response['entry']


def test_error_handling_in_update_view(dummy_request):
    """Test that the on HTTPNotFound is raised if not found."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


# @pytest.fixture
# def testapp():
#     """Functional test for app."""
#     from webtest import TestApp
#     from pyramid.config import Configurator

#     def main():
#         config = Configurator()
#         config.include('pyramid_jinja2')
#         config.include('.routes')
#         config.scan()
#         return config.make_wsgi_app()

#     app = main()
#     return TestApp(app)


# def test_home_route_has_all_journal_entries(testapp):
#     """Test that the home route all journal entries."""
#     from pyramid_learning_journal.data.entry_history import ENTRIES
#     response = testapp.get("/")
#     assert len(ENTRIES) == len(response.html.find_all('div', 'card'))


# def test_deatil_route_has_one_entry(testapp):
#     """Test that the detail_view shows one journal entry."""
#     from pyramid_learning_journal.data.entry_history import ENTRIES
#     response = testapp.get("/journal/1")
#     assert len(response.html.find_all('div', 'card')) == 1
#     assert ENTRIES[0]['title'] in response.text


# def test_create_view_has_a_create_button(testapp):
#     """Test that the Create page has a 'Create' button."""
#     response = testapp.get("/journal/new-entry")
#     assert len(response.html.find_all('button', attrs={"type": "submit"})) == 1
#     assert "Create" in response.html.find('button', attrs={"type": "submit"})


# def test_update_view_has_an_update_button(testapp):
#     """Test that the Update page has a 'Update' button."""
#     response = testapp.get("/journal/1/edit-entry")
#     assert len(response.html.find_all('button', attrs={"type": "submit"})) == 1
#     assert "Update" in response.html.find('button', attrs={"type": "submit"})
