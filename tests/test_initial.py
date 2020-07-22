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
        yield (
            actual_file_path,
            expected_file_path,
            expected_dir_path,
            expected_img_path,
        )


@pytest.fixture()
def prepare_hexlet():
    with tempfile.TemporaryDirectory() as tmpdirname:
        actual_file_path = save_page(
            'https://ru.hexlet.io/courses',
            tmpdirname,
        )
        expected_file_path = os.path.join(
            tmpdirname,
            'ru-hexlet-io-courses.html',
        )
        expected_dir_path = os.path.join(
            tmpdirname,
            'ru-hexlet-io-courses_files',
        )
        yield (
            actual_file_path,
            expected_file_path,
            expected_dir_path,
        )


def test_exists(prepare_regexp, prepare_hexlet):
    (
        actual_file_path,
        expected_file_path,
        expected_dir_path,
        expected_img_path,
    ) = prepare_regexp
    assert os.path.isfile(actual_file_path)
    assert expected_file_path == actual_file_path
    assert os.path.isdir(expected_dir_path)
    assert os.path.isfile(expected_img_path)

    (
        actual_file_path,
        expected_file_path,
        expected_dir_path,
    ) = prepare_hexlet
    assert os.path.isfile(actual_file_path)
    assert expected_file_path == actual_file_path
    assert os.path.isdir(expected_dir_path)
