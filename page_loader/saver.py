import logging
import os
import re
import time

import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

from page_loader.modifier import KnownError, make_name, parse_url

TAGS = (SCRIPT, LINK, IMAGE) = ('script', 'link', 'img')
ATTRIBUTES = (SRC, HREF) = ('src', 'href')
LOCAL_LINKS = re.compile(r'^(?!(\/|.+\/{2}))(?=\/?\w+)')


def get_response(url, stream=None):
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
    _, domain = parse_url(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    with IncrementalBar('Scripts saving', max=10) as bar:
        for item in range(10):
            time.sleep(0.10)
            bar.next()
    scripts_soup = save_src(
        soup, domain, dir,
        tag=SCRIPT,
    )
    with IncrementalBar('Links saving', max=10) as bar:
        for item in range(10):
            time.sleep(0.10)
            bar.next()
    links_soup = save_src(
        scripts_soup, domain, dir,
        tag=LINK,
    )
    with IncrementalBar('Images saving', max=10) as bar:
        for item in range(10):
            time.sleep(0.10)
            bar.next()
    images_soup = save_src(
        links_soup, domain, dir,
        tag=IMAGE,
    )
    return images_soup.prettify()


def save_src(soup, domain, dir, tag):
    if tag in [SCRIPT, IMAGE]:
        attr = SRC
        attrs = {SRC: LOCAL_LINKS}
    elif tag == LINK:
        attr = HREF
        attrs = {HREF: LOCAL_LINKS}
    for resource in soup.find_all(tag, attrs):
        src_to_load = os.path.join(domain, resource.get(attr))
        if tag in [SCRIPT, LINK]:
            src_data = get_response(src_to_load)
        elif tag == IMAGE:
            src_data = get_response(src_to_load, stream=True)
        name, extension = os.path.splitext(resource.get(attr))
        file_name = make_name(name, extension)
        output_full_path = os.path.join(dir, file_name)
        if tag == IMAGE:
            with open(output_full_path, 'wb') as feature:
                try:
                    for chunk in src_data.iter_content(chunk_size=128):
                        feature.write(chunk)
                except OSError as err:
                    logging.debug(err, exc_info=True)
                    logging.error(
                        "Can't save image, %s. An error occurred: %s",
                        output_full_path,
                        err,
                    )
        elif tag in [SCRIPT, LINK]:
            with open(output_full_path, 'w') as feature:
                try:
                    feature.write(src_data.text)
                except OSError as err:
                    logging.debug(err, exc_info=True)
                    logging.error(
                        "Can't save %s, %s. An error occurred: %s",
                        tag,
                        output_full_path,
                        err,
                    )
        logging.info('\u2713 %s', src_to_load)
        resource[attr] = output_full_path
        logging.info('%s replaced with: %s', tag, resource[attr])
    return soup
