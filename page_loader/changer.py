import os
import re
import logging


class KnownError(Exception):
    pass


def get_path(url):
    if url[:8] == 'https://':
        path = url[8:]
    elif url[:7] == 'http://':
        path = url[7:]
    else:
        path = url
    if path[:3] == 'www':
        path = path[4:]
    return path


def get_domain(url):
    path = get_path(url)
    domain = re.match(r'^[\w\.-]+', path)
    return 'https://' + domain.group(0)


def change_name(path):
    divider = '-'
    old_name = get_path(path)
    new_name = re.sub(r'[\W_]', divider, old_name)
    return new_name


def make_name(path, extension):
    return change_name(path) + extension


def make_dir(path, output_path):
    dir_name = os.path.join(output_path, make_name(path, '_files'))
    try:
        os.mkdir(dir_name)
    except OSError as error:
        logging.debug('An error occurred: %s', error)
        logging.error(
            'Directory you are trying to create (%s) already exists',
            dir_name,
        )
        raise KnownError() from error
    return dir_name
