import os
import tempfile
from page_loader.loader import get_page


def test_initial():
    with tempfile.TemporaryDirectory() as tmpdirname:
        exp_path1 = os.path.join(tmpdirname, 'hexlet-io-courses.html')
        exp_path2 = os.path.join(tmpdirname, 'ru-hexlet-io-courses.html')
        assert exp_path1 == get_page(
            'https://hexlet.io/courses',
            tmpdirname,
        )
        assert True == os.path.exists(get_page(
            'https://hexlet.io/courses',
            tmpdirname,
        ))
        assert exp_path2 == get_page(
            'https://ru.hexlet.io/courses',
            tmpdirname,
        )
        assert True == os.path.exists(get_page(
            'https://ru.hexlet.io/courses',
            tmpdirname,
        ))
