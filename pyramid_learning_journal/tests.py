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


def test_update_view_get_returns_only_one_entry_detail(dummy_request, add_entries):
    """Test that the Update view function returns one entry by id."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert add_entries[0].to_dict() == response['entry']


def test_update_view_get_returns_correct_entry_details(dummy_request, add_entries):
    """Test that the update view function returns the correct entry data."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 1
    response = update_view(dummy_request)
    assert response['entry']['id'] == 1


def test_update_view_get_raises_httpnotfound_for_bad_id(dummy_request, add_entries):
    """Test that update_view raises HTTPNotFound if index out of bounds."""
    from pyramid_learning_journal.views.default import update_view
    dummy_request.matchdict['id'] = 99
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


def test_update_view_post_updates_entry(dummy_request, add_entry):
    """Test that the entry is updated on update_view POST, not created."""
    from pyramid_learning_journal.views.default import update_view
    from pyramid_learning_journal.models import Entry
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    update_view(dummy_request)
    assert dummy_request.dbsession.query(Entry).count() == 1


def test_update_view_post_updates_entry_with_given_info(dummy_request, add_entry):
    """Test that entry updated uses POST info on update_view POST."""
    from pyramid_learning_journal.views.default import update_view
    from pyramid_learning_journal.models import Entry
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data

    old_entry = dummy_request.dbsession.query(Entry).get(1).to_dict()
    update_view(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(1)
    assert entry.title == entry_data['title']
    assert entry.body == entry_data['body']
    assert entry.title != old_entry['title']
    assert entry.body != old_entry['body']


def test_update_view_post_has_302_status_code(dummy_request, add_entry):
    """Test that update_view POST has 302 status code."""
    from pyramid_learning_journal.views.default import update_view
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    response = update_view(dummy_request)
    assert response.status_code == 302


def test_update_view_post_redirects_to_detail_with_httpfound(dummy_request, add_entry):
    """Test that update_view POST redirects to detail of id with httpfound."""
    from pyramid_learning_journal.views.default import update_view
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    response = update_view(dummy_request)
    assert isinstance(response, HTTPFound)
    assert response.location == dummy_request.route_url('detail', id=1)


def test_update_view_post_incompelete_data_is_bad_request(dummy_request, add_entry):
    """Test that update_view POST with incomplete data is invalid."""
    from pyramid_learning_journal.views.default import update_view
    entry_data = {
        'title': 'not fun times'
    }
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    with pytest.raises(HTTPBadRequest):
        update_view(dummy_request)


def test_update_view_post_raises_httpnotfound_for_bad_id(dummy_request, add_entry):
    """Test that update_view raises HTTPNotFound if index out of bounds."""
    from pyramid_learning_journal.views.default import update_view
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    dummy_request.matchdict['id'] = 99
    dummy_request.method = 'POST'
    dummy_request.POST = entry_data
    with pytest.raises(HTTPNotFound):
        update_view(dummy_request)


def test_delete_journal_entry_get_raises_httpnotfound(dummy_request, add_entries):
    """Test that delete_journal_entry raises HTTPNotFound for a GET request."""
    from pyramid_learning_journal.views.default import delete_journal_entry
    dummy_request.matchdict['id'] = 1
    with pytest.raises(HTTPNotFound):
        delete_journal_entry(dummy_request)


def test_delete_journal_entry_post_deletes_entry(dummy_request, add_entries):
    """Test that the entry is deleted on delete_journal_entry POST."""
    from pyramid_learning_journal.views.default import delete_journal_entry
    from pyramid_learning_journal.models import Entry

    assert dummy_request.dbsession.query(Entry).count() == len(add_entries)
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    delete_journal_entry(dummy_request)
    assert dummy_request.dbsession.query(Entry).count() == len(add_entries) - 1


def test_delete_journal_entry_post_deletes_entry_with_id(dummy_request, add_entries):
    """Test that entry deleted is the one with the given id."""
    from pyramid_learning_journal.views.default import delete_journal_entry
    from pyramid_learning_journal.models import Entry
    entry = dummy_request.dbsession.query(Entry).all()[0]
    assert entry.id == 1

    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    delete_journal_entry(dummy_request)

    assert entry not in dummy_request.dbsession.query(Entry).all()


def test_delete_journal_entry_post_has_302_status_code(dummy_request, add_entries):
    """Test that delete_journal_entry POST has 302 status code."""
    from pyramid_learning_journal.views.default import delete_journal_entry
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    response = delete_journal_entry(dummy_request)
    assert response.status_code == 302


def test_delete_journal_entry_post_redirects_to_home_with_httpfound(dummy_request, add_entries):
    """Test that delete_journal_entry POST redirects to home with httpfound."""
    from pyramid_learning_journal.views.default import delete_journal_entry
    dummy_request.matchdict['id'] = 1
    dummy_request.method = 'POST'
    response = delete_journal_entry(dummy_request)
    assert isinstance(response, HTTPFound)
    assert response.location == dummy_request.route_url('home')


def test_delete_journal_entry_post_raises_httpnotfound_for_bad_id(dummy_request, add_entries):
    """Test that delete_journal_entry POST raises HTTPNotFound for a invalid id."""
    from pyramid_learning_journal.views.default import delete_journal_entry
    dummy_request.matchdict['id'] = 99
    dummy_request.method = 'POST'
    with pytest.raises(HTTPNotFound):
        delete_journal_entry(dummy_request)


""" FUNCTIONAL TESTS FOR ROUTES """


def test_home_route_gets_200_status_code(testapp, fill_the_db):
    """Test that the home route gets 200 status code."""
    response = testapp.get("/")
    assert response.status_code == 200


def test_home_route_has_all_journal_entries(testapp, test_entries):
    """Test that the home route all journal entries."""
    response = testapp.get("/")
    assert len(test_entries) == len(response.html.find_all('div', 'card'))


def test_detail_route_has_one_entry(testapp):
    """Test that the detail route shows one journal entry."""
    response = testapp.get("/journal/1")
    assert len(response.html.find_all('div', 'card')) == 1


def test_detail_route_for_valid_id_gets_200_status_code(testapp):
    """Test that the detail route of a valid gets 200 status code."""
    response = testapp.get("/journal/1")
    assert response.status_code == 200


def test_detail_route_has_correct_entry(testapp):
    """Test that the detail route shows correct journal entry."""
    response = testapp.get("/journal/1")
    assert 'Day 0' in response.html.find('h2')


def test_detail_route_goes_to_404_page_for_invalid_id(testapp):
    """Test that the detail route redirects to 404 page for invalid id."""
    response = testapp.get("/journal/-1", status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_update_get_route_for_valid_id_gets_200_status_code(testapp):
    """Test that GET to update route of a valid gets 200 status code."""
    response = testapp.get("/journal/1/edit-entry")
    assert response.status_code == 200


def test_update_get_route_has_filled_form(testapp):
    """Test that the Update page has a filled form."""
    response = testapp.get("/journal/1/edit-entry")
    assert len(response.html.find_all('input', attrs={"type": "text"})) == 1
    assert 'value="Day 0"' in str(response.html.find('input', attrs={"type": "text"}))


def test_update_get_route_has_an_update_button(testapp):
    """Test that the Update page has a 'Update' button."""
    response = testapp.get("/journal/1/edit-entry")
    assert len(response.html.find_all('button', attrs={"type": "submit"})) == 1
    assert "Update" in response.html.find('button', attrs={"type": "submit"})


def test_update_get_route_goes_to_404_page_for_invalid_id(testapp):
    """Test that the update GET route redirects to 404 page for invalid id."""
    response = testapp.get("/journal/-1/edit-entry", status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_update_post_route_updates_correct_entry(testapp, testapp_session):
    """Test that POST to update route updates a entry."""
    from pyramid_learning_journal.models import Entry
    entry_data = {
        'title': 'so it begins',
        'body': 'the beginning of change'
    }
    old_entry = testapp_session.query(Entry).get(1).to_dict()
    testapp.post("/journal/1/edit-entry", entry_data)
    entry = testapp_session.query(Entry).get(1)
    assert entry.title == entry_data['title']
    assert entry.body == entry_data['body']
    assert entry.title != old_entry['title']
    assert entry.body != old_entry['body']


def test_update_post_route_has_a_302_status_code(testapp):
    """Test that POST to update route gets a 302 status code."""
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    response = testapp.post("/journal/1/edit-entry", entry_data)
    assert response.status_code == 302


def test_update_post_route_redirects_to_detail_route_for_id(testapp):
    """Test that POST to update route redirects to detail for the given id."""
    entry_data = {
        'title': 'fun times 2',
        'body': 'all the fun, all the time. x 2'
    }
    response = testapp.post("/journal/1/edit-entry", entry_data)
    detail = testapp.app.routes_mapper.get_route('detail').generate({'id': 1})
    assert response.location.endswith(detail)


def test_update_post_route_adds_new_entry_to_home(testapp):
    """Test that the new entry is on the home page after POST to update."""
    entry_data = {
        'title': 'fun times 4',
        'body': 'all the fun, all the time. x 4'
    }
    response = testapp.post("/journal/1/edit-entry", entry_data)
    next_page = response.follow()
    assert entry_data['title'] in next_page.html.find('h2')
    assert entry_data['body'] in str(next_page.html.find('div', 'card-text'))


def test_update_post_route_has_400_error_for_incomplete_data(testapp):
    """Test that POST of incomplete data to update causes 400 error."""
    from webtest import AppError
    entry_data = {
        'title': 'fun times 8'
    }
    with pytest.raises(AppError) as err:
        testapp.post("/journal/1/edit-entry", entry_data)
    assert '400' in err.value.args[0]


def test_update_post_route_goes_to_404_page_for_invalid_id(testapp):
    """Test that the update POST route redirects to 404 page for invalid id."""
    entry_data = {
        'title': 'the end',
        'body': 'last of the updates.'
    }
    response = testapp.post("/journal/-1/edit-entry", entry_data, status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_delete_get_route_goes_to_404_page(testapp):
    """Test that the delete GET route redirects to 404 page."""
    response = testapp.get("/journal/1/delete-entry", status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_delete_post_route_deletes_correct_entry(testapp, testapp_session):
    """Test that POST to delete route deletes a entry."""
    from pyramid_learning_journal.models import Entry
    entry = testapp_session.query(Entry).get(1)
    testapp.post("/journal/1/delete-entry")
    assert entry not in testapp_session.query(Entry).all()


def test_delete_post_route_has_a_302_status_code(testapp):
    """Test that POST to delete route gets a 302 status code."""
    response = testapp.post("/journal/2/delete-entry")
    assert response.status_code == 302


def test_delete_post_route_redirects_to_home_route(testapp):
    """Test that POST to delete route redirects to home route."""
    response = testapp.post("/journal/3/delete-entry")
    home = testapp.app.routes_mapper.get_route('home').path
    assert response.location.endswith(home)


def test_delete_post_route_removes_entry_to_home(testapp, test_entries):
    """Test that the entry is gone from the home page after POST to delete."""
    response = testapp.post("/journal/4/delete-entry")
    next_page = response.follow()
    assert 'Day 3' not in next_page.html.find_all('h2')[-1]
    assert len(next_page.html.find_all('h2')) == len(test_entries) - 4


def test_delete_route_removes_detail_page_for_id(testapp):
    """Test that the delete route also removes access to detail page for id."""
    testapp.get("/journal/5")
    testapp.post("/journal/5/delete-entry")

    response = testapp.get("/journal/5", status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_delete_post_route_goes_to_404_page_for_invalid_id(testapp):
    """Test that the delete POST route redirects to 404 page for invalid id."""
    response = testapp.post("/journal/-1/delete-entry", status=404)
    assert 'Oops' in str(response.html.find('h1'))


def test_create_get_route_gets_200_status_code(testapp):
    """Test that GET to create route gets 200 status code."""
    response = testapp.get("/journal/new-entry")
    assert response.status_code == 200


def test_create_get_route_has_empty_form(testapp):
    """Test that the Create page has an empty form."""
    response = testapp.get("/journal/new-entry")
    assert len(response.html.find_all('input', attrs={"type": "text"})) == 1
    assert 'value' not in response.html.find('input', attrs={"type": "text"})


def test_create_get_route_has_a_create_button(testapp):
    """Test that the Create page has a 'Create' button."""
    response = testapp.get("/journal/new-entry")
    assert len(response.html.find_all('button', attrs={"type": "submit"})) == 1
    assert "Create" in response.html.find('button', attrs={"type": "submit"})


def test_create_post_route_adds_a_new_entry(testapp, empty_the_db, testapp_session):
    """Test that POST to create route creates a new entry."""
    from pyramid_learning_journal.models import Entry
    assert len(testapp_session.query(Entry).all()) == 0
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    testapp.post("/journal/new-entry", entry_data)
    assert len(testapp_session.query(Entry).all()) == 1


def test_create_post_route_has_a_302_status_code(testapp, empty_the_db):
    """Test that POST to create route gets a 302 status code."""
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    response = testapp.post("/journal/new-entry", entry_data)
    assert response.status_code == 302


def test_create_post_route_redirects_to_home_route(testapp, empty_the_db):
    """Test that POST to create route redirects to home route."""
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    response = testapp.post("/journal/new-entry", entry_data)
    home = testapp.app.routes_mapper.get_route('home').path
    assert response.location.endswith(home)


def test_create_post_route_adds_new_entry_to_home(testapp, empty_the_db):
    """Test that the new entry is on the home page after POST to create."""
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    response = testapp.post("/journal/new-entry", entry_data)
    next_page = response.follow()
    assert entry_data['title'] in next_page.html.find('h2')
    assert entry_data['body'] in str(next_page.html.find('div', 'card-text'))


def test_create_post_route_allows_access_to_detail_page(testapp, empty_the_db):
    """Test that the new entry has an available detail page."""
    from webtest import AppError
    with pytest.raises(AppError):
        testapp.get("/journal/1")

    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    testapp.post("/journal/new-entry", entry_data)
    testapp.get("/journal/1")


def test_create_post_route_new_detail_page_has_new_info(testapp, empty_the_db):
    """Test that the detail page for new entry has the correct info."""
    entry_data = {
        'title': 'fun times',
        'body': 'all the fun, all the time.'
    }
    testapp.post("/journal/new-entry", entry_data)
    response = testapp.get("/journal/1")
    assert entry_data['title'] in response.html.find('h2')
    assert entry_data['body'] in str(response.html.find('div', 'card-text'))


def test_create_post_route_has_400_error_for_incomplete_data(testapp):
    """Test that POST of incomplete data to create causes 400 error."""
    from webtest import AppError
    entry_data = {
        'title': 'fun times'
    }
    with pytest.raises(AppError) as err:
        testapp.post("/journal/new-entry", entry_data)
    assert '400' in err.value.args[0]
