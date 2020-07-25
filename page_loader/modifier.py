import logging
import os
import re
from urllib.parse import urlparse, urlunparse


class KnownError(Exception):
    pass


def parse_url(url):
    parsed_url = urlparse(url)
    domain = os.path.join('https://', parsed_url.netloc.strip('/'))
    if parsed_url.netloc == '':
        domain = os.path.join('https://', url)
        return url, domain
    elif parsed_url.netloc[:3] == 'www':
        path = urlunparse(parsed_url._replace(
            scheme='',
            netloc=parsed_url.netloc[4:])
        ).strip('/')
        return path, domain
    path = urlunparse(parsed_url._replace(scheme='')).strip('/')
    return path, domain


def change_name(path):
    divider = '-'
    new_name = re.sub(r'[\W_]', divider, path)
    return new_name


def make_name(url, extension):
    path_to_file, _ = parse_url(url)
    return change_name(path_to_file) + extension


def make_dir(dir, url):
    path_to_dir, _ = parse_url(url)
    dir_name = os.path.join(dir, make_name(path_to_dir, '_files'))
    try:
        os.mkdir(dir_name)
    except OSError as error:
        logging.debug('An error occurred: %s', error, exc_info=True)
        logging.error(
            'Directory you are trying to create (%s) already exists',
            dir_name,
        )
        raise KnownError() from error
    else:
        logging.info('Created directory: %s', dir_name)
        return dir_name
