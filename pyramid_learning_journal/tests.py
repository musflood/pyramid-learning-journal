"""Unit tests basic response test for all view functions."""


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
    assert 'Home</title>' in list_view(dummy_request).text


def test_detail_view_returns_response(dummy_request):
    """Test that our detail view reutrns a Response."""
    from pyramid_learning_journal.views.default import detail_view
    assert isinstance(detail_view(dummy_request), Response)


def test_detail_view_responds_with_200_status_code(dummy_request):
    """Test that our detail view res[onds with a proper 200 status code."""
    from pyramid_learning_journal.views.default import detail_view
    assert detail_view(dummy_request).status_code == 200


def test_detail_view_has_proper_content(dummy_request):
    """Test that our detail view Response has proper content."""
    from pyramid_learning_journal.views.default import detail_view
    assert 'Entry Detail</title>' in detail_view(dummy_request).text


def test_create_view_returns_response(dummy_request):
    """Test that our create view reutrns a Response."""
    from pyramid_learning_journal.views.default import create_view
    assert isinstance(create_view(dummy_request), Response)


def test_create_view_responds_with_200_status_code(dummy_request):
    """Test that our create view res[onds with a proper 200 status code."""
    from pyramid_learning_journal.views.default import create_view
    assert create_view(dummy_request).status_code == 200


def test_create_view_has_proper_content(dummy_request):
    """Test that our create view Response has proper content."""
    from pyramid_learning_journal.views.default import create_view
    assert 'New Entry</title>' in create_view(dummy_request).text


def test_update_view_returns_response(dummy_request):
    """Test that our update view reutrns a Response."""
    from pyramid_learning_journal.views.default import update_view
    assert isinstance(update_view(dummy_request), Response)


def test_update_view_responds_with_200_status_code(dummy_request):
    """Test that our update view res[onds with a proper 200 status code."""
    from pyramid_learning_journal.views.default import update_view
    assert update_view(dummy_request).status_code == 200


def test_update_view_has_proper_content(dummy_request):
    """Test that our update view Response has proper content."""
    from pyramid_learning_journal.views.default import update_view
    assert 'Edit Entry</title>' in update_view(dummy_request).text
