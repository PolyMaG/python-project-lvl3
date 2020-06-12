import os
import tempfile
import requests
from page_loader.loader import save_page


def test_initial():
    with tempfile.TemporaryDirectory() as tmpdirname:
        exp_file = os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers.html',
        )
        assert exp_file == save_page(
            'https://www.regular-expressions.info/modifiers.html',
            tmpdirname,
        )
        assert True == os.path.exists(save_page(
            'https://www.regular-expressions.info/modifiers.html',
            tmpdirname,
        ))
        assert True == os.path.exists(os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers_files',
            'ads-728-rxbtutorial100.png',
        ))
        loaded_data = requests.get('https://www.regular-expressions.info/regex.js')
        with open(os.path.join(tmpdirname, 'regex.js'), 'w') as feature:
            feature.write(loaded_data.text)
        with open(os.path.join(tmpdirname, 'regex.js'), 'r') as feature:
            expected = feature.read()
        with open(os.path.join(
            tmpdirname,
            'regular-expressions-info-modifiers_files',
            'regex.js',
        ), 'r') as fixture:
            actual = fixture.read()
        assert expected == actual
