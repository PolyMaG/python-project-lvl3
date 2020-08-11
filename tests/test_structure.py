import os
import tempfile

import pytest

from page_loader.loader import save_page


@pytest.fixture()
def prepare_regexp():
    with tempfile.TemporaryDirectory() as tmpdirname:
        actual_file_path = save_page(
            'https://www.regular-expressions.info/modifiers.html',
            tmpdirname,
        )
        expected_file_path = os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers-html.html',
        )
        expected_dir_path = os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers-html_files',
        )
        expected_img_path = os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers-html_files',
            'ads-728-rxbtutorial100.png',
        )
        expected_css_path = os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers-html_files',
            'regex.css',
        )
        expected_js_path = os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers-html_files',
            'regex.js',
        )
        yield (
            actual_file_path,
            expected_file_path,
            expected_dir_path,
            expected_img_path,
            expected_css_path,
            expected_js_path,
        )


def test_structure(prepare_regexp):
    (
        actual_file_path,
        expected_file_path,
        expected_dir_path,
        expected_img_path,
        expected_css_path,
        expected_js_path,
    ) = prepare_regexp
    assert os.path.isfile(actual_file_path)
    assert expected_file_path == actual_file_path
    assert os.path.isdir(expected_dir_path)
    assert os.path.isfile(expected_img_path)
    assert os.path.isfile(expected_css_path)
    assert os.path.isfile(expected_js_path)
