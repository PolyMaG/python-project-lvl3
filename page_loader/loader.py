import os
import re
import requests
import logging
from bs4 import BeautifulSoup


def get_path(url):
    root, _ = os.path.splitext(url)
    if root[:8] == 'https://':
        path = root[8:]
    elif root[:7] == 'http://':
        path = root[7:]
    else:
        path = root
    if path[:3] == 'www':
        path = path[4:]
    return path


def get_domain(url):
    path = get_path(url)
    ext = re.search(r'(\.\w+)(?=\/\w+)', path)
    domain_name, _ = re.split(r'\.\w+\/', path)
    domain = 'https://' + domain_name + ext.group(0)
    return domain


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
        logging.error('An error occurred: %s', error)
    return dir_name


def get_source_data(url):
    return requests.get(url)


def save_resources(url, saved_page, dir_name):
    soup = BeautifulSoup(saved_page, "html.parser")
    for resource in soup.find_all(
        ["script", "img"],
        src=re.compile(r'^\/?(?!(\/|.+\/{2}))'),  # find local links
    ):
        domain = get_domain(url)
        path_to_load = os.path.join(domain, resource.get('src'))
        loaded_data = get_source_data(path_to_load)
        name, extension = os.path.splitext(resource.get('src'))
        file_name = make_name(name, extension)
        output_full_path = os.path.join(dir_name, file_name)
        if extension == '.jpg' or extension == '.png':
            with open(output_full_path, 'wb') as feature:
                feature.write(loaded_data.content)
        else:
            with open(output_full_path, 'w') as feature:
                feature.write(loaded_data.text)
        resource['src'] = output_full_path
        logging.info('Replaced images and scripts: %s', resource['src'])
    return soup.prettify()


def save_links(url, new_page, dir_name):
    soup = BeautifulSoup(new_page, "html.parser")
    for resource in soup.find_all(
        "link",
        href=re.compile(r'^\/?(?!(\/|.+\/{2}))'),  # find local links
    ):
        domain = get_domain(url)
        path_to_load = os.path.join(domain, resource.get('href'))
        loaded_data = get_source_data(path_to_load)
        name, extension = os.path.splitext(resource.get('href'))
        file_name = make_name(name, extension)
        output_full_path = os.path.join(dir_name, file_name)
        with open(output_full_path, 'w') as feature:
            feature.write(loaded_data.text)
        resource['href'] = output_full_path
        logging.info('Replaced links: %s', resource['href'])
    return soup.prettify()


def save_page(url, output_path):
    source_data = get_source_data(url)
    path = get_path(url)
    file_name = make_name(path, '.html')
    dir_name = make_dir(path, output_path)
    logging.info('Created directory: %s', dir_name)
    output_full_path = os.path.join(output_path, file_name)
    with open(output_full_path, 'w') as feature:
        feature.write(source_data.text)
    logging.info('Saved page: %s', output_full_path)
    with open(output_full_path, 'r') as feature:
        saved_page = feature.read()
    with open(output_full_path, 'w') as feature:
        feature.write(save_resources(url, saved_page, dir_name))
    with open(output_full_path, 'r') as feature:
        new_page = feature.read()
    with open(output_full_path, 'w') as feature:
        feature.write(save_links(url, new_page, dir_name))
    return output_full_path
