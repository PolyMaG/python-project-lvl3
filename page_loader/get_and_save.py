import logging

import requests

from page_loader.helpers import KnownError


def response(url, stream=None):
    """
    Get response object.

    Args:
        url (string): URL to get as a response.
        stream (optional):
            If True - you get raw socket response
            (for downloading images). Defaults to None.

    Raises:
        KnownError.

    Returns:
        object: Response object.
    """
    try:
        response = requests.get(url, stream=None)
        response.raise_for_status()
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.RequestException,
    ) as exc:
        logging.debug(exc, exc_info=True)
        logging.error('An error occurred: %s', exc)
        raise KnownError() from exc
    else:
        return response


def text(data_to_save, path_to_file):
    """
    Save given textdata to a file.

    Args:
        data_to_save (string): Textdata to save.
        path_to_file (string): Where to save.

    Returns:
        string: Path to saved file.
    """
    with open(path_to_file, 'w') as feature:
        try:
            feature.write(data_to_save)
        except OSError as err:
            logging.debug(err, exc_info=True)
            logging.error(
                "Can't save %s. An error occurred: %s",
                path_to_file,
                err,
            )
        else:
            return path_to_file


def save_image(image_data, path_to_file):
    """
    Save given image to file.

    Args:
        image_data (object): Raw socket response.
        path_to_file (string): Where to save.

    Returns:
        string: Path to saved file.
    """
    with open(path_to_file, 'wb') as feature:
        try:
            for chunk in image_data.iter_content(chunk_size=128):
                feature.write(chunk)
        except OSError as err:
            logging.debug(err, exc_info=True)
            logging.error(
                "Can't save image, %s. An error occurred: %s",
                path_to_file,
                err,
            )
        else:
            return path_to_file


def data(*args):
    """
    Download text data from given URL (url_to_save)
    and save it to given path (full_file_path).

    Args:
        args (dict): Keys - URL to load data from,
            Values - path to save downloaded data.
    """
    for arg in args:
        for url_to_save, full_file_path in arg.items():
            try:
                src_data = response(url_to_save)
                text(src_data.text, full_file_path)
            except Exception as err:
                logging.debug(err, exc_info=True)
                logging.error('Unexpected error occurred: %s', err)
            finally:
                logging.info('\u2713 %s', url_to_save)


def image(images):
    """
    Download image data from given URL (url_to_save)
    and save it to given path (full_file_path).

    Args:
        images (dict): Keys - URL to load image from,
            Values - path to save downloaded image.
    """
    for url_to_save, full_file_path in images.items():
        try:
            src_data = response(url_to_save, stream=True)
            save_image(src_data, full_file_path)
        except Exception as error:
            logging.debug(error, exc_info=True)
            logging.error('Unexpected error occurred: %s', error)
        finally:
            logging.info('\u2713 %s', url_to_save)
