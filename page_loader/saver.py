import os
import re
import time
import logging
import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from page_loader.changer import KnownError
from page_loader.changer import make_name, get_domain


local_links = re.compile(r'^(?!(\/|.+\/{2}))(?=\/?\w+)')


def data(url, stream=None):
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
        raise KnownError from exc
    else:
        return response


def resources(url, html, dir_name):
    domain = get_domain(url)
    soup = BeautifulSoup(html, "html.parser")
    with IncrementalBar('Scripts saving', max=10) as bar:
        for i in range(10):
            time.sleep(0.15)
            bar.next()
    saved_scripts = scripts(soup, domain, dir_name)
    with IncrementalBar('Links saving', max=10) as bar:
        for i in range(10):
            time.sleep(0.15)
            bar.next()
    saved_links = links(saved_scripts, domain, dir_name)
    with IncrementalBar('Images saving', max=10) as bar:
        for i in range(10):
            time.sleep(0.15)
            bar.next()
    saved_images = images(saved_links, domain, dir_name)
    return saved_images.prettify()


def scripts(soup, domain, dir_name):
    for resource in soup.find_all(
        "script",
        src=local_links,
    ):
        url_to_load = os.path.join(domain, resource.get('src'))
        loaded_data = data(url_to_load)
        name, extension = os.path.splitext(resource.get('src'))
        file_name = make_name(name, extension)
        output_full_path = os.path.join(dir_name, file_name)
        with open(output_full_path, 'w') as feature:
            try:
                feature.write(loaded_data.text)
            except OSError as err:
                logging.debug(err, exc_info=True)
                logging.error(
                    "Can't save script, %s. An error occurred: %s",
                    output_full_path,
                    err,
                )
                # raise KnownError from err
        logging.info('\u2713 %s', url_to_load)
        resource['src'] = output_full_path
        logging.info('Saved script replaced with: %s', resource['src'])
    return soup


def links(soup, domain, dir_name):
    for resource in soup.find_all(
        "link",
        href=local_links,
    ):
        url_to_load = os.path.join(domain, resource.get('href'))
        loaded_data = data(url_to_load)
        name, extension = os.path.splitext(resource.get('href'))
        file_name = make_name(name, extension)
        output_full_path = os.path.join(dir_name, file_name)
        with open(output_full_path, 'w') as feature:
            try:
                feature.write(loaded_data.text)
            except OSError as err:
                logging.debug(err, exc_info=True)
                logging.error(
                    "Can't save link, %s. An error occurred: %s",
                    output_full_path,
                    err,
                )
                # raise KnownError from err
        logging.info('\u2713 %s', url_to_load)
        resource['href'] = output_full_path
        logging.info('Saved link replaced with: %s', resource['href'])
    return soup


def images(soup, domain, dir_name):
    for resource in soup.find_all(
        "img",
        src=local_links,
    ):
        url_to_load = os.path.join(domain, resource.get('src'))
        loaded_data = data(url_to_load, stream=True)
        name, extension = os.path.splitext(resource.get('src'))
        file_name = make_name(name, extension)
        output_full_path = os.path.join(dir_name, file_name)
        with open(output_full_path, 'wb') as feature:
            try:
                for chunk in loaded_data.iter_content(chunk_size=128):
                    feature.write(chunk)
            except OSError as err:
                logging.debug(err, exc_info=True)
                logging.error(
                    "Can't save image, %s. An error occurred: %s",
                    output_full_path,
                    err,
                )
                # raise KnownError from err
        logging.info('\u2713 %s', url_to_load)
        resource['src'] = output_full_path
        logging.info('Saved image replaced with: %s', resource['src'])
    return soup
