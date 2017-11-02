from pyramid.view import view_config
from pyramid_learning_journal.data import entry_history
from pyramid.exceptions import HTTPNotFound


@view_config(route_name='home', renderer='pyramid_learning_journal:templates/list_view.jinja2')
def list_view(request):
    """List of journal entries."""
    return {
        "entries": sorted(entry_history.ENTRIES, key=lambda e: -e['id']),
        "page_title": "Home"
    }


@view_config(route_name='detail', renderer='pyramid_learning_journal:templates/detail.jinja2')
def detail_view(request):
    """A single journal entry."""
    entry_id = int(request.matchdict['id'])
    if entry_id < 0 or entry_id > len(entry_history.ENTRIES):
        raise HTTPNotFound
    entry = list(filter(lambda entry: entry['id'] == entry_id, entry_history.ENTRIES))[0]
    return {
        "page_title": "Entry Detail",
        "entry": entry
    }


@view_config(route_name='create', renderer='pyramid_learning_journal:templates/create.jinja2')
def create_view(request):
    """Create a new entry."""
    return {
        "page_title": "New Entry"
    }


@view_config(route_name='edit', renderer='pyramid_learning_journal:templates/edit.jinja2')
def update_view(request):
    """Update an existing entry."""
    entry_id = int(request.matchdict['id'])
    if entry_id < 0 or entry_id > len(entry_history.ENTRIES):
        raise HTTPNotFound
    entry = list(filter(lambda entry: entry['id'] == entry_id, entry_history.ENTRIES))[0]
    return {
        "page_title": "Edit Entry",
        "entry": entry
    }
