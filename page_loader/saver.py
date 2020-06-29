import logging
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader.changer import KnownError, get_domain, make_name

local_links = re.compile(r'^(?!(\/|.+\/{2}))(?=\/?\w+)')


def url_data(url, stream=None):
    try:
        response = requests.get(url, stream=None)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        logging.debug('Connection error: %s', exc, exc_info=True)
        logging.error('Connection error occurred: %s', exc)
        raise KnownError() from exc
    except requests.exceptions.HTTPError as exc:
        logging.debug('HTTP response error: %s', exc, exc_info=True)
        logging.error('HTTP response error occurred: %s', exc)
        raise KnownError() from exc
    except requests.exceptions.RequestException as exc:
        logging.debug('An error occurred: %s', exc, exc_info=True)
        logging.error('Some error occurred: %s', exc)
        raise KnownError() from exc
    else:
        return response


def resources(url, html_doc, dir):
    domain = get_domain(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    with IncrementalBar('Scripts saving', max=10) as bar:
        for item in range(10):
            time.sleep(0.15)
            bar.next()
    saved_scripts_soup = scripts(soup, domain, dir)
    with IncrementalBar('Links saving', max=10) as bar:
        for item in range(10):
            time.sleep(0.15)
            bar.next()
    saved_links_soup = links(saved_scripts_soup, domain, dir)
    with IncrementalBar('Images saving', max=10) as bar:
        for item in range(10):
            time.sleep(0.15)
            bar.next()
    saved_images_soup = images(saved_links_soup, domain, dir)
    return saved_images_soup.prettify()


def scripts(soup, domain, dir):
    for resource in soup.find_all(
        'script',
        src=local_links,
    ):
        src_to_load = os.path.join(domain, resource.get('src'))
        src_data = url_data(src_to_load)
        name, extension = os.path.splitext(resource.get('src'))
        file_name = make_name(name, extension)
        output_full_path = os.path.join(dir, file_name)
        with open(output_full_path, 'w') as feature:
            try:
                feature.write(src_data.text)
            except OSError as err:
                logging.debug(err, exc_info=True)
                logging.error(
                    "Can't save script, %s. An error occurred: %s",
                    output_full_path,
                    err,
                )
        logging.info('\u2713 %s', src_to_load)
        resource['src'] = output_full_path
        logging.info('Saved script replaced with: %s', resource['src'])
    return soup


def links(soup, domain, dir):
    for resource in soup.find_all(
        'link',
        href=local_links,
    ):
        src_to_load = os.path.join(domain, resource.get('href'))
        src_data = url_data(src_to_load)
        name, extension = os.path.splitext(resource.get('href'))
        file_name = make_name(name, extension)
        output_full_path = os.path.join(dir, file_name)
        with open(output_full_path, 'w') as feature:
            try:
                feature.write(src_data.text)
            except OSError as err:
                logging.debug(err, exc_info=True)
                logging.error(
                    "Can't save link, %s. An error occurred: %s",
                    output_full_path,
                    err,
                )
        logging.info('\u2713 %s', src_to_load)
        resource['href'] = output_full_path
        logging.info('Saved link replaced with: %s', resource['href'])
    return soup


def images(soup, domain, dir):
    for resource in soup.find_all(
        'img',
        src=local_links,
    ):
        src_to_load = os.path.join(domain, resource.get('src'))
        src_data = url_data(src_to_load, stream=True)
        name, extension = os.path.splitext(resource.get('src'))
        file_name = make_name(name, extension)
        output_full_path = os.path.join(dir, file_name)
        with open(output_full_path, 'wb') as feature:
            try:
                for chunk in src_data.item_content(chunk_size=128):
                    feature.write(chunk)
            except OSError as err:
                logging.debug(err, exc_info=True)
                logging.error(
                    "Can't save image, %s. An error occurred: %s",
                    output_full_path,
                    err,
                )
        logging.info('\u2713 %s', src_to_load)
        resource['src'] = output_full_path
        logging.info('Saved image replaced with: %s', resource['src'])
    return soup
