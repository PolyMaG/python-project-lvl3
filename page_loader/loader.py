import os
import time
import logging
from progress.bar import IncrementalBar
import page_loader.saver as save
from page_loader.changer import cut_url, make_name, make_dir


def save_page(url, output_path):
    page_data = save.data(url)
    path = cut_url(url)
    file_name = make_name(path, '.html')
    dir_name = make_dir(path, output_path)
    logging.info('Created directory: %s', dir_name)
    output_full_path = os.path.join(output_path, file_name)
    with open(output_full_path, 'w') as feature:
        try:
            with IncrementalBar('Page saving', max=1) as bar:
                for i in range(1):
                    time.sleep(0.15)
                    bar.next()
            feature.write(page_data.text)
            logging.info(
                '\u2713 Page was downloaded as %s',
                output_full_path,
            )
        except OSError as err:
            logging.debug(err, exc_info=True)
            logging.error("Can't save the page. An error occurred: %s", err)
    with open(output_full_path, 'r') as feature:
        try:
            saved_page = feature.read()
        except OSError as err:
            logging.debug(err, exc_info=True)
            logging.error("Can't read saved page: %s", err)
    with open(output_full_path, 'w') as feature:
        try:
            feature.write(save.resources(url, saved_page, dir_name))
        except OSError as err:
            logging.debug(err, exc_info=True)
            logging.error(
                "Something went wrong while saving resources: %s",
                err,
            )
    return output_full_path
