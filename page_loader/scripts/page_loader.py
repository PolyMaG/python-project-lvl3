#!/usr/bin/env python3
import argparse
import logging
import os
import sys

from page_loader.modifier import KnownError
from page_loader.loader import save_page


FORMAT = '%(levelname)s: %(message)s'


def parser(arg_list):
    parser = argparse.ArgumentParser(description='page-loader')
    parser.add_argument(
        '-o', '--output',
        default='.',
        help='set the directory to save to',
    )
    parser.add_argument(
        '--loglevel',
        default='INFO',
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
        help='set the level of log message severity',
    )
    parser.add_argument('url')
    return parser


def main():
    args = parser(sys.argv[1:]).parse_args()
    logging.basicConfig(
        level=logging.DEBUG,
        format=FORMAT,
        filename=os.path.join(args.output, 'logfile.log'),
        filemode='w',
    )
    console = logging.StreamHandler()
    console.setLevel(args.loglevel)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info('Started.')
    try:
        save_page(args.url, args.output)
    except KnownError:
        logging.error('Program has stopped.')
        sys.exit(1)
    else:
        logging.info('Finished.')


if __name__ == '__main__':
    main()
