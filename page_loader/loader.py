import logging
import os

import page_loader.get_and_save as get_and_save
from page_loader.helpers import make_dir, make_name, parse_html


def save_page(url, output_dir):
    """
    Download html and local resources.

    Args:
        url (string): URL to download.
        output_dir (string): Place to save.

    Returns:
        string: Saved page URL.
    """
    page_data = get_and_save.response(url)
    dir_to_save = make_dir(output_dir, url)
    file_name = make_name(url, '.html')
    path_to_save = os.path.join(output_dir, file_name)
    (
        html_to_save,
        scripts_to_save,
        links_to_save,
        images_to_save
    ) = parse_html(url, page_data.text, dir_to_save)
    saved_page = get_and_save.text(
        html_to_save,
        path_to_save,
    )
    get_and_save.data(scripts_to_save, links_to_save)
    get_and_save.image(images_to_save)
    logging.info(
        "\nPage was downloaded as '%s'",
        path_to_save,
    )
    return saved_page
