import os
import tempfile
from page_loader.loader import save_page


def test_exists_regexp():
    with tempfile.TemporaryDirectory() as tmpdirname:
        actual_file = save_page(
            'https://www.regular-expressions.info/modifiers.html',
            tmpdirname,
        )
        expected_file = os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers-html.html',
        )
        expected_dir = os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers-html_files',
        )
        expected_img = os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers-html_files',
            'ads-728-rxbtutorial100.png',
        )
        assert os.path.isfile(actual_file)
        assert expected_file == actual_file
        assert os.path.isdir(expected_dir)
        assert os.path.isfile(expected_img)


def test_exists_hexlet():
    with tempfile.TemporaryDirectory() as tmpdirname:
        actual_file = save_page(
            'https://ru.hexlet.io/courses',
            tmpdirname,
        )
        expected_file = os.path.join(
            tmpdirname,
            'ru-hexlet-io-courses.html',
        )
        expected_dir = os.path.join(
            tmpdirname,
            'ru-hexlet-io-courses_files',
        )
        assert os.path.isfile(actual_file)
        assert expected_file == actual_file
        assert os.path.isdir(expected_dir)
