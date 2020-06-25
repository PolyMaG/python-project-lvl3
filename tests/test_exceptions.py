import tempfile
import pytest
from page_loader.changer import KnownError
from page_loader.loader import save_page


def test_existing_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(KnownError):
            save_page(
                'https://www.regular-expressions.info/modifiers.html',
                tmpdirname,
            )
            assert save_page(
                'https://www.regular-expressions.info/modifiers.html',
                tmpdirname,
            )


def test_connection_problems():
    with tempfile.TemporaryDirectory() as tmpdirname:
        pytest.raises(
            KnownError,
            save_page,
            'https://www.bla-bla.com',
            tmpdirname,
        )


def test_http_response_problems():
    with tempfile.TemporaryDirectory() as tmpdirname:
        pytest.raises(
            KnownError,
            save_page,
            'https://www.regular-expressions.info/modifier.html',
            tmpdirname,
        )
