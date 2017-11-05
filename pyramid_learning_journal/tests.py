"""Tests for the pyramid_learning_journal package."""

from __future__ import unicode_literals
from pyramid.exceptions import HTTPNotFound
import pytest


""" UNIT TESTS FOR MODELS """


def test_constructed_entry_with_no_date_added_to_database(db_session):
    """Test that Entry constructed with no date gets added to the database."""
    from pyramid_learning_journal.models import Entry
    assert len(db_session.query(Entry).all()) == 0
    entry = Entry(
        title='test 1',
        body='this is a test'
    )
    db_session.add(entry)
    assert len(db_session.query(Entry).all()) == 1


""" UNIT TESTS FOR VIEW FUNCTIONS """


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
    """Test that detail_view raises HTTPNotFound if index out of bounds."""
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
    """Test that update_view raises HTTPNotFound if index out of bounds."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


def test_error_handling_in_delete_journal_entry(dummy_request, test_entry):
    """Test that delete_journal_entry raises HTTPNotFound for a GET rquest."""
    from pyramid_learning_journal.views.default import delete_journal_entry
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        delete_journal_entry(dummy_request)


""" FUNCTIONAL TESTS FOR ROUTES """


def test_home_route_has_all_journal_entries(testapp, fill_the_db, test_entries):
    """Test that the home route all journal entries."""
    response = testapp.get("/")
    assert len(test_entries) == len(response.html.find_all('div', 'card'))


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
