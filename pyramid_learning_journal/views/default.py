from pyramid.view import view_config
from pyramid.exceptions import HTTPNotFound
from pyramid_learning_journal.models import Entry


@view_config(route_name='home', renderer='pyramid_learning_journal:templates/list_view.jinja2')
def list_view(request):
    """List of journal entries."""
    entries = request.dbsession.query(Entry).all()
    entries = sorted(entries, key=lambda e: e.creation_date, reverse=True)
    entries = [entry.to_html_dict() for entry in entries]
    return {
        "entries": entries,
        "page_title": "Home"
    }


@view_config(route_name='detail', renderer='pyramid_learning_journal:templates/detail.jinja2')
def detail_view(request):
    """A single journal entry."""
    entry_id = int(request.matchdict['id'])

    entry = request.dbsession.query(Entry).get(entry_id)

    if entry:
        return {
            "page_title": entry.title,
            "entry": entry.to_html_dict()
        }
    raise HTTPNotFound


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

    entry = request.dbsession.query(Entry).get(entry_id)

    if entry:
        return {
            "page_title": "Edit '{}'".format(entry.title),
            "entry": entry.to_dict()
        }
    raise HTTPNotFound
