"""Tests for the pyramid_learning_journal package."""

from __future__ import unicode_literals
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from datetime import datetime
from pytz import utc
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


def test_constructed_entry_with_no_date_has_date_set_to_now():
    """Test that Entry constructed with no date uses now for creation_date."""
    from pyramid_learning_journal.models import Entry
    entry = Entry(
        title='test 1',
        body='this is a test'
    )
    now = datetime.now(utc)
    assert now.strftime('%c') == entry.creation_date.strftime('%c')


def test_constructed_entry_with_date_added_to_database(db_session):
    """Test that Entry constructed with no date gets added to the database."""
    from pyramid_learning_journal.models import Entry
    assert len(db_session.query(Entry).all()) == 0
    entry = Entry(
        title='test 1',
        body='this is a test',
        creation_date=datetime(2017, 10, 12, 1, 30)
    )
    db_session.add(entry)
    assert len(db_session.query(Entry).all()) == 1


def test_constructed_entry_with_date_has_given_date():
    """Test that Entry constructed with date uses it for creation_date."""
    from pyramid_learning_journal.models import Entry
    entry = Entry(
        title='test 1',
        body='this is a test',
        creation_date=datetime(2017, 10, 12, 1, 30)
    )
    date = datetime(2017, 10, 12, 1, 30)
    assert date.strftime('%c') == entry.creation_date.strftime('%c')


def test_to_dict_puts_all_properties_in_a_dictionary(test_entry):
    """Test that all properties of an Entry are in to_dict dictionary."""
    entry_dict = test_entry.to_dict()
    assert all(prop in entry_dict for prop in ['id', 'title', 'body', 'creation_date'])


def test_to_dict_leaves_body_in_markdown(test_entry):
    """Test that an Entry's body is in markdown in to_dict dictionary."""
    entry_dict = test_entry.to_dict()
    assert entry_dict['body'] == test_entry.body


def test_to_dict_converts_date_to_string(test_entry):
    """Test that an Entry's creation_date is a string in to_dict dicitonary."""
    entry_dict = test_entry.to_dict()
    assert isinstance(entry_dict['creation_date'], str)


def test_to_html_dict_puts_all_properties_in_a_dictionary(test_entry):
    """Test that all properties of an Entry are in to_html_dict dictionary."""
    entry_dict = test_entry.to_html_dict()
    assert all(prop in entry_dict for prop in ['id', 'title', 'body', 'creation_date'])


def test_to_html_dict_leaves_body_in_markdown(test_entry):
    """Test that an Entry's body is in markdown in to_html_dict."""
    entry_dict = test_entry.to_html_dict()
    assert entry_dict['body'].startswith('<p>')
    assert entry_dict['body'].endswith('</p>')


def test_to_html_dict_converts_date_to_string(test_entry):
    """Test that an Entry's creation_date is a string in to_html_dict."""
    entry_dict = test_entry.to_html_dict()
    assert isinstance(entry_dict['creation_date'], str)


""" UNIT TESTS FOR VIEW FUNCTIONS """


def test_list_view_returns_list(dummy_request, add_entries):
    """Test that the list view function returns a list of the entries."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert 'entries' in response
    assert isinstance(response['entries'], list)


def test_list_view_returns_entries_in_list(dummy_request, add_entries):
    """Test that the list view function returns entries as dicitonaries."""
    from pyramid_learning_journal.views.default import list_view
    response = list_view(dummy_request)
    assert add_entries[0].to_html_dict() in response['entries']


def test_list_view_returns_all_entries_in_db(dummy_request, add_entries):
    """Test that the list view function returns all entries in database."""
    from pyramid_learning_journal.views.default import list_view
    from pyramid_learning_journal.models import Entry
    response = list_view(dummy_request)
    query = dummy_request.dbsession.query(Entry)
    assert len(response['entries']) == query.count()


def test_detail_view_returns_one_entry_detail(dummy_request, add_entries):
    """Test that the detail view function returns the data of one entry."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert add_entries[0].to_html_dict() == response['entry']


def test_detail_view_returns_correct_entry_detail(dummy_request, add_entries):
    """Test that the detail view function returns the correct entry data."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 1
    response = detail_view(dummy_request)
    assert response['entry']['id'] == 1


def test_detail_view_raises_httpnotfound_for_bad_id(dummy_request, add_entries):
    """Test that detail_view raises HTTPNotFound if index out of bounds."""
    from pyramid_learning_journal.views.default import detail_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        detail_view(dummy_request)


def test_create_view_get_returns_only_the_page_title(dummy_request):
    """Test that the new entry function returns only page title for GET."""
    from pyramid_learning_journal.views.default import create_view
    response = create_view(dummy_request)
    assert 'page_title' in response
    assert 'New Entry' == response['page_title']


def test_create_view_post_creates_new_entry(dummy_request):
    """Test that the new entry is created on create_view POST."""
    from pyramid_learning_journal.views.default import create_view
    from pyramid_learning_journal.models import Entry
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    create_view(dummy_request)
    assert dummy_request.dbsession.query(Entry).count() == 1


def test_create_view_post_creates_new_entry_with_given_info(dummy_request):
    """Test that new entry created uses POST info on create_view POST."""
    from pyramid_learning_journal.views.default import create_view
    from pyramid_learning_journal.models import Entry
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    create_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(1)
    assert entry.title == entry_data['title']
    assert entry.body == entry_data['body']


def test_create_view_post_has_302_status_code(dummy_request):
    """Test that create_view POST has 302 status code."""
    from pyramid_learning_journal.views.default import create_view
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    response = create_view(dummy_request)
    assert response.status_code == 302


def test_create_view_post_redirects_to_home_with_httpfound(dummy_request):
    """Test that create_view POST redirects to home with httpfound."""
    from pyramid_learning_journal.views.default import create_view
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    response = create_view(dummy_request)
    assert isinstance(response, HTTPFound)
    assert response.location == dummy_request.route_url('home')


def test_create_view_post_incompelete_data_is_bad_request(dummy_request):
    """Test that create_view POST with incomplete data is invalid."""
    from pyramid_learning_journal.views.default import create_view
    entry_data = {
        'title': 'not fun times'
    }
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    with pytest.raises(HTTPBadRequest):
        create_view(dummy_request)


def test_update_view_returns_only_one_entry_detail(dummy_request, add_entries):
    """Test that the Update view function returns one entry by id."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert add_entries[0].to_dict() == response['entry']


def test_update_view_raises_httpnotfound_for_bad_id(dummy_request, add_entries):
    """Test that update_view raises HTTPNotFound if index out of bounds."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


def test_delete_entry_raises_httpnotfound_for_bad_id(dummy_request, add_entries):
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
