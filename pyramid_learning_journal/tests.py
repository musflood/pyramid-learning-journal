"""Unit tests basic response test for all view functions."""

from pyramid.exceptions import HTTPNotFound
from pyramid.testing import DummyRequest
import pytest


@pytest.fixture
def dummy_request():
    """Create a dummy GET request."""
    return DummyRequest()


def test_list_entries_returns_list_of_entries_in_dict(dummy_request):
    """Test that the list view function returns a list of all the dict entries."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert 'entries' in response
    assert isinstance(response['entries'], list)


def test_detail_entry_returns_one_detail_entry_in_dict(dummy_request):
    """Test that the detail view function returns a full view of one of the dict entries."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert 'entry' in response
    assert isinstance(response['entry'], dict)


def test_create_entry_returns_a_response_for_new_entry(dummy_request):
    """Test that the new entry function returns a value from a new item."""
    from pyramid_learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert 'page_title' in response
    assert 'New Entry' == response['page_title']


def test_update_view_returns_list_of_entries_in_dict(dummy_request):
    """Test that the Update view function returns a key in the dict."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert 'entry' in response
    assert isinstance(response['entry'], dict)


@pytest.fixture
def testapp():
    """Functional test for app."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main():
        config = Configurator()
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main()
    return TestApp(app)


def test_home_route_has_table(testapp):
    """Test that the home route has a table."""
    from pyramid_learning_journal.data.entry_history import ENTRIES
    response = testapp.get("/")
    assert len(ENTRIES) == len(response.html.find_all('div', 'card'))


def test_error_handling_in_detail_view(dummy_request):
    """Test that the on HTTPNotFound is raised if not found."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_error_handling_in_update_view(dummy_request):
    """Test that the on HTTPNotFound is raised if not found."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)
