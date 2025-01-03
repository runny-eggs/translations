"""
Tests for the validate_translation_files.py script.
"""

import os.path
import re

from ..validate_translation_files import (
    get_translation_files,
    validate_translation_files,
)

SCRIPT_DIR = os.path.dirname(__file__)


def test_get_translation_files():
    """
    Ensure `get_translation_files` skips the source translation files and non-po files.
    """
    mock_translations_dir = os.path.join(SCRIPT_DIR, 'mock_translations_dir')
    po_files_sorted = sorted(get_translation_files(mock_translations_dir))
    relative_po_files = [
        os.path.relpath(po_file, SCRIPT_DIR)
        for po_file in po_files_sorted
    ]

    assert relative_po_files == [
        'mock_translations_dir/demo-xblock/conf/locale/ar/LC_MESSAGES/django.po',
        'mock_translations_dir/demo-xblock/conf/locale/de_DE/LC_MESSAGES/django.po',
        'mock_translations_dir/demo-xblock/conf/locale/hi/LC_MESSAGES/django.po',
    ]


def test_main_on_invalid_files(capsys):
    """
    Integration test for the `main` function on some invalid files.
    """
    mock_translations_dir = os.path.join(SCRIPT_DIR, 'mock_translations_dir')
    exit_code = validate_translation_files(mock_translations_dir)
    out, err = capsys.readouterr()

    assert 'VALID:' in out, 'Valid files should be printed in stdout'
    assert 'de_DE/LC_MESSAGES/django.po' in out, 'German translation file should be found valid'
    assert 'ar/LC_MESSAGES/django.po' in out, 'Arabic translation file should be found valid'
    assert 'hi/LC_MESSAGES/django.po' not in out, 'Invalid file should be printed in stderr'
    assert 'en/LC_MESSAGES/django.po' not in out, 'Source file should not be validated'

    assert re.match(r'INVALID: .*hi/LC_MESSAGES/django.po', err)
    assert '\'msgstr\' is not a valid Python brace format string, unlike \'msgid\'' in err
    assert 'FAILURE: Some translations are invalid.' in err

    assert exit_code == 1, 'Should fail due to invalid hi/LC_MESSAGES/django.po file'


def test_main_on_valid_files(capsys):
    """
    Integration test for the `main` function but only for the Arabic translations which is valid.
    """
    mock_translations_dir = os.path.join(SCRIPT_DIR, 'mock_translations_dir/demo-xblock/conf/locale/ar')
    exit_code = validate_translation_files(mock_translations_dir)
    out, err = capsys.readouterr()

    assert 'VALID:' in out, 'Valid files should be printed in stdout'
    assert 'ar/LC_MESSAGES/django.po' in out, 'Arabic translation file is valid'
    assert 'SUCCESS: All translation files are valid.' in out
    assert not err.strip(), 'The stderr should be empty'
    assert exit_code == 0, 'Should succeed due in validating the ar/LC_MESSAGES/django.po file'
