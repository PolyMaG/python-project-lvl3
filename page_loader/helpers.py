import logging
import os
import re
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup

TAGS = (SCRIPT, LINK, IMAGE) = ('script', 'link', 'img')
LOCAL_PATTERN = r'^([^http|\/\/][\w]*[\.|\/].+)'


class KnownError(Exception):
    """Define empty KnownError."""

    pass


def parse_url(url):
    """
    URL parser.

    Args:
        url (string): URL to parse.

    Returns:
        tuple:
            path: URL without scheme and 'www'.
            domain: Domain name with 'https' scheme, i.e. 'https://google.com'.
    """
    parsed_url = urlparse(url)
    domain = os.path.join('https://', parsed_url.netloc.strip('/'))
    if parsed_url.netloc == '':
        domain = os.path.join('https://', url)
        return url, domain
    elif parsed_url.netloc[:3] == 'www':
        path = urlunparse(parsed_url._replace(
            scheme='',
            netloc=parsed_url.netloc[4:],
        ),
        ).strip('/')
        return path, domain
    path = urlunparse(parsed_url._replace(scheme='')).strip('/')
    return path, domain


def change_name(old_name):
    """
    Replace non-word and figures char. in given name to a divider-char.

    Args:
        old_name (string): Name to change.

    Returns:
        string: New name.
    """
    divider = '-'
    new_name = re.sub(r'[\W_]', divider, old_name)
    return new_name


def make_name(url, extension):
    """
    Change name and add given extension.

    Args:
        url (string): URL from which you extract path to make name.
        extension (string): Extension to add to name.

    Returns:
        string: New name with given extension.
    """
    name_path, _ = parse_url(url)
    return change_name(name_path) + extension


def make_dir(dir, url):
    """
    Create directory.

    Args:
        dir (string): First part of dir name.
        url (string): URL where you get second part for dir name.

    Raises:
        KnownError: Directory already exists.

    Returns:
        string: Directory name.
    """
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
        return dir_name


def generate_url_and_path(domain, resource, dir):
    # make a valid url to load data from source
    url_to_save = os.path.join(domain, resource.group(0))
    #  generate full local path for loaded resource
    name, extension = os.path.splitext(resource.group(0))
    file_name = make_name(name, extension)
    local_path = os.path.join(dir, file_name)
    return url_to_save, local_path


def parse_html(url, html_doc, dir):
    """
    Find local resources and replace its names.

    Find local resources in given tags,
    replace path to resource to a local one.

    Args:
        url (string): [Description]
        html_doc (string): html to parse.
        dir (string): [description]

    Returns:
        object: BeautifulSoup object with replaced links.
        dict: Keys - local resources (scripts, links, images) URL,
            Values - replaced paths to a local ones.
    """
    scripts_to_save = {}
    links_to_save = {}
    images_to_save = {}
    _, domain = parse_url(url)
    soup = BeautifulSoup(html_doc, "html.parser")
    for tag in soup.find_all(TAGS):
        if tag.name == SCRIPT and tag.get('src'):
            local_script = re.match(LOCAL_PATTERN, tag.get('src'))
            if local_script:
                url_to_save, local_path = generate_url_and_path(
                    domain, local_script, dir)
                #  replace saved resource name with a local one
                tag['src'] = local_path
                scripts_to_save[url_to_save] = local_path
        elif tag.has_attr('href') and tag.get('href'):
            local_link = re.match(LOCAL_PATTERN, tag.get('href'))
            if local_link:
                url_to_save, local_path = generate_url_and_path(
                    domain, local_link, dir)
                tag['href'] = local_path
                links_to_save[url_to_save] = local_path
        elif tag.name == IMAGE and tag.get('src'):
            local_image = re.match(LOCAL_PATTERN, tag.get('src'))
            if local_image:
                url_to_save, local_path = generate_url_and_path(
                    domain, local_image, dir)
                tag['src'] = local_path
                images_to_save[url_to_save] = local_path
    return soup.prettify(), scripts_to_save, links_to_save, images_to_save
