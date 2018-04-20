from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPBadRequest
from pyramid_learning_journal.models import Entry
from pyramid.security import remember, forget
from pyramid_learning_journal.security import check_credentials


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


@view_config(
    route_name='create',
    renderer='pyramid_learning_journal:templates/create.jinja2',
    permission='secret'
)
def create_view(request):
    """Create a new entry."""
    if request.method == 'GET':
        return {
            "page_title": "New Entry"
        }

    if request.method == 'POST':
        if not all([field in request.POST for field in ['title', 'body']]):
            raise HTTPBadRequest
        new_entry = Entry(
            title=request.POST['title'],
            body=request.POST['body']
        )
        request.dbsession.add(new_entry)
        return HTTPFound(request.route_url('home'))


@view_config(
    route_name='edit',
    renderer='pyramid_learning_journal:templates/edit.jinja2',
    permission='secret'
)
def update_view(request):
    """Update an existing entry."""
    entry_id = int(request.matchdict['id'])

    entry = request.dbsession.query(Entry).get(entry_id)

    if not entry:
        raise HTTPNotFound

    if request.method == 'GET':
        return {
            "page_title": "Edit '{}'".format(entry.title),
            "entry": entry.to_dict()
        }

    if request.method == 'POST':
        if not all([field in request.POST for field in ['title', 'body']]):
            raise HTTPBadRequest
        entry.title = request.POST['title']
        entry.body = request.POST['body']
        request.dbsession.add(entry)
        request.dbsession.flush()
        return HTTPFound(request.route_url('detail', id=entry_id))


@view_config(route_name='delete', permission='secret')
def delete_journal_entry(request):
    """Delete a journal entry."""
    if request.method == 'GET':
        raise HTTPNotFound

    entry_id = int(request.matchdict['id'])

    entry = request.dbsession.query(Entry).get(entry_id)

    if not entry:
        raise HTTPNotFound

    if request.method == 'POST':
        request.dbsession.delete(entry)
        return HTTPFound(request.route_url('home'))


@view_config(route_name='login', renderer='pyramid_learning_journal:templates/login.jinja2')
def login(request):
    """Login to the learning journal to get authenticated."""
    if request.authenticated_userid:
        return HTTPFound(request.route_url('home'))

    if request.method == 'GET':
        return {"page_title": "Login"}

    if request.method == 'POST':
        if 'username' not in request.POST or 'password' not in request.POST:
            raise HTTPBadRequest
        username = request.POST['username']
        password = request.POST['password']
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(request.route_url('home'), headers=headers)
        return {
            "page_title": "Login",
            'error': 'The username and/or password are incorrect.'
        }


@view_config(route_name='logout', permission='secret')
def logout(request):
    """Logout of the learning journal, remove authorization."""
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)
