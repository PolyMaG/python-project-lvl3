import os
import tempfile
import requests
from page_loader.loader import save_page


def test_save_resources():
    with tempfile.TemporaryDirectory() as tmpdirname:
        save_page(
            'https://www.regular-expressions.info/modifiers.html',
            tmpdirname,
        )
        expected_data = requests.get(
            'https://www.regular-expressions.info/regex.js')
        with open(os.path.join(tmpdirname, 'regex.js'), 'w') as feature:
            feature.write(expected_data.text)
        with open(os.path.join(tmpdirname, 'regex.js'), 'r') as feature:
            expected = feature.read()
        with open(os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers-html_files',
            'regex.js',
        ), 'r') as fixture:
            actual = fixture.read()
        assert expected == actual
