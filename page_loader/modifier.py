import logging
import os
import re
from urllib.parse import urlparse, urlunparse


class KnownError(Exception):
    pass


def cut_url(url):
    u = urlparse(url)
    if u.netloc == '':
        return url
    elif u.netloc[:3] == 'www':
        return urlunparse(u._replace(scheme='', netloc=u.netloc[4:]))[2:]
    return urlunparse(u._replace(scheme=''))[2:]


def get_domain(url):
    u = urlparse('//' + cut_url(url))
    return urlunparse(
        u._replace(
            scheme='https',
            path='',
            params='',
            query='',
            fragment='',
        )
    )


def change_name(path):
    divider = '-'
    old_name = cut_url(path)
    new_name = re.sub(r'[\W_]', divider, old_name)
    return new_name


def make_name(url, extension):
    path = cut_url(url)
    return change_name(path) + extension


def make_dir(dir, url):
    path = cut_url(url)
    dir_name = os.path.join(dir, make_name(path, '_files'))
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
