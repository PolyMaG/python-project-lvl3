import os
import tempfile

import pytest
import requests

from page_loader.helpers import parse_html
from page_loader.loader import save_page


def prepare_regexp():
    with tempfile.TemporaryDirectory() as tmpdirname:
        save_page(
            'https://www.regular-expressions.info/modifiers.html',
            tmpdirname,
        )
        expected_data = requests.get(
            'https://www.regular-expressions.info/regex.js')
        with open(os.path.join(tmpdirname, 'regex.js'), 'w') as fixture:
            fixture.write(expected_data.text)
        with open(os.path.join(tmpdirname, 'regex.js'), 'r') as fixture:
            expected = fixture.read()
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


def test_html():
    with open('./tests/fixtures/test1.html') as fixture:
        test_html = fixture.read()
    expected_links = {
        'https://bla-bla.com/regex.css':
        '/var/tmp/bla-bla-com-foo-html_files/regex.css'
    }
    expected_scripts = {
        'https://bla-bla.com/regex.js':
        '/var/tmp/bla-bla-com-foo-html_files/regex.js'
    }
    expected_images = {
        'https://bla-bla.com/ads/728/rxbtutorial100.png':
        '/var/tmp/bla-bla-com-foo-html_files/ads-728-rxbtutorial100.png'
    }
    (_, scripts, links, images) = parse_html(
        'http://bla-bla.com/foo.html',
        test_html,
        '/var/tmp/bla-bla-com-foo-html_files',
    )
    assert expected_links == links
    assert expected_scripts == scripts
    assert expected_images == images
