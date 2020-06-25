import os
import logging
import page_loader.saver as save
from page_loader.changer import KnownError
from page_loader.changer import get_path, make_name, make_dir


def save_page(url, output_path):
    page_data = save.data(url)
    path = get_path(url)
    file_name = make_name(path, '.html')
    dir_name = make_dir(path, output_path)
    logging.info('Created directory: %s', dir_name)
    output_full_path = os.path.join(output_path, file_name)
    with open(output_full_path, 'w') as feature:
        try:
            feature.write(page_data.text)
            logging.info('Page has been saved with name: %s', output_full_path)
        except OSError as err:
            logging.error("Can't save the page. An error occurred: %s", err)
            raise KnownError() from err
    with open(output_full_path, 'r') as feature:
        try:
            saved_page = feature.read()
        except OSError as err:
            logging.error("Can't read saved page: %s", err)
            # raise KnownError() from err
    with open(output_full_path, 'w') as feature:
        try:
            feature.write(save.resources(url, saved_page, dir_name))
        except OSError as err:
            logging.error(
                "Something went wrong while saving resources: %s",
                err,
            )
    return output_full_path
