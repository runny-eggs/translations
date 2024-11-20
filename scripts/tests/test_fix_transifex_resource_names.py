"""
Tests for fix_transifex_resource_names.py.
"""

from unittest.mock import MagicMock
from ..fix_transifex_resource_names import get_repo_slug_from_resource


def test_get_repo_slug_from_resource_with_no_categories():
    resource = MagicMock()
    resource.slug = 'translations-my-xblock-conf-locale-en-lc-messages-django-po--main'
    resource.categories = []
    assert get_repo_slug_from_resource(resource) == 'my-xblock'


def test_get_repo_slug_from_resource_slug_js_with_no_categories():
    resource = MagicMock()
    resource.slug = 'translations-my-xblock-conf-locale-en-lc-messages-djangojs-po--main'
    resource.categories = []
    assert get_repo_slug_from_resource(resource) == 'my-xblock-js'


def test_get_repo_name_from_invalid_slug():
    resource = MagicMock()
    resource.slug = 'some-gibberish-slug'
    resource.categories = []
    assert get_repo_slug_from_resource(resource) == None


def test_get_repo_name_from_slug_and_categories():
    """
    Categories takes precedence over slug.
    """
    resource = MagicMock()
    resource.slug = 'translations-my-xblock1-conf-locale-en-lc-messages-django-po--main'
    resource.categories = ['github#repository:openedx/openedx-translations#branch:main#path:translations/my-xblock2/openassessment/conf/locale/en/LC_MESSAGES/django.po']  # noqa
    assert get_repo_slug_from_resource(resource) == 'my-xblock2'


def test_get_repo_name_from_categories():
    resource = MagicMock()
    resource.slug = 'some-gibberish-slug'
    resource.categories = ['github#repository:openedx/openedx-translations#branch:main#path:translations/my-xblock2/openassessment/conf/locale/en/LC_MESSAGES/django.po']  # noqa
    assert get_repo_slug_from_resource(resource) == 'my-xblock2'


def test_get_repo_name_from_categories_with_js():
    resource = MagicMock()
    resource.slug = 'some-gibberish-slug'
    resource.categories = ['github#repository:openedx/openedx-translations#branch:main#path:translations/my-xblock2/openassessment/conf/locale/en/LC_MESSAGES/djangojs.po']  # noqa
    assert get_repo_slug_from_resource(resource) == 'my-xblock2-js'
