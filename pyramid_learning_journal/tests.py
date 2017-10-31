"""."""


import pytest
from pyramid.testing import DummyRequest
from pyramid.response import Response


@pytest.fixture
def dummy_request():
    """Create a dummy GET request."""
    return DummyRequest()


def test_list_view_returns_response(dummy_request):
    """Test that our list view reutrns a Response."""
    from pyramid_learning_journal.views.default import list_view
    assert isinstance(list_view(dummy_request), Response)


def test_list_view_responds_with_200_status_code(dummy_request):
    """Test that our list view res[onds with a proper 200 status code."""
    from pyramid_learning_journal.views.default import list_view
    assert list_view(dummy_request).status_code == 200


def test_list_view_has_proper_content(dummy_request):
    """Test that our list view Response has proper content."""
    from pyramid_learning_journal.views.default import list_view
    assert '<title>Python Learning Journal | Home</title>' in list_view(dummy_request).text
