import os
import tempfile

import pytest
import requests

from page_loader.loader import save_page


def prepare_regexp():
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
        return (expected, actual)


@pytest.mark.parametrize(
    "expected,actual",
    [(prepare_regexp()[0], prepare_regexp()[1])]
)
def test_regexp(expected, actual):
    assert expected == actual
