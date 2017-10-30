from pyramid.response import Response
import os

HERE = os.path.abspath(__file__)
STATIC = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'static')
TEMPLATES = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'templates')


def list_view(request):
    """List of journal entries."""
    with open(os.path.join(TEMPLATES, 'index.html')) as file:
        return Response(file.read())


def detail_view(request):
    """A single journal entry."""
    pass


def create_view(request):
    """Create a new entry."""
    pass


def update_view(request):
    """Update an existing entry."""
    pass
