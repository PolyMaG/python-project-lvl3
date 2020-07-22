import logging
import os
import time

from progress.bar import IncrementalBar

import page_loader.saver as save
from page_loader.modifier import make_dir, make_name


def prepare_data(url, output_dir):
    page_data = save.get_response(url)
    dir_to_save = make_dir(output_dir, url)
    file_name = make_name(url, '.html')
    output_full_path = os.path.join(output_dir, file_name)
    return output_full_path, page_data, dir_to_save


def save_page(url, output_dir):
    output_full_path, page_data, dir_to_save = prepare_data(url, output_dir)
    saved_page_html = open_page(save_html(output_full_path, page_data))
    saved_page_with_resources = save_resources(
        output_full_path,
        url,
        saved_page_html,
        dir_to_save,
    )
    return saved_page_with_resources


def save_html(output_full_path, page_data):
    with open(output_full_path, 'w') as feature:
        try:
            with IncrementalBar('Page saving', max=10) as bar:
                for item in range(10):
                    time.sleep(0.05)
                    bar.next()
            feature.write(page_data.text)
        except OSError as err:
            logging.debug(err, exc_info=True)
            logging.error("Can't save the page. An error occurred: %s", err)
        else:
            logging.info(
                '\u2713 Page was downloaded as %s',
                output_full_path,
            )
            return output_full_path


def open_page(output_full_path):
    with open(output_full_path, 'r') as feature:
        try:
            saved_page = feature.read()
        except OSError as err:
            logging.debug(err, exc_info=True)
            logging.error("Can't read saved page: %s", err)
        else:
            return saved_page


def save_resources(output_full_path, url, html_doc, dir_to_save):
    with open(output_full_path, 'w') as feature:
        try:
            feature.write(save.resources(url, html_doc, dir_to_save))
        except OSError as err:
            logging.debug(err, exc_info=True)
            logging.error(
                'Something went wrong while saving resources: %s',
                err,
            )
        else:
            return output_full_path
