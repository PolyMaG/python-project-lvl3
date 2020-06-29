import logging
import os
import re


class KnownError(Exception):
    pass


def cut_url(url):
    if url[:8] == 'https://':
        cutted_url = url[8:]
    elif url[:7] == 'http://':
        cutted_url = url[7:]
    else:
        cutted_url = url
    if cutted_url[:3] == 'www':
        cutted_url = cutted_url[4:]
    return cutted_url


def get_domain(url):
    cutted_url = cut_url(url)
    domain = re.match(r'^[\w\.-]+', cutted_url)
    return 'https://' + domain.group(0)


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
