from pyramid.view import view_config


@view_config(route_name='home', renderer='pyramid_learning_journal:templates/list_view.jinja2')
def list_view(request):
    """List of journal entries."""
    pass


def detail_view(request):
    """A single journal entry."""
    pass


def create_view(request):
    """Create a new entry."""
    pass


def update_view(request):
    """Update an existing entry."""
    pass
