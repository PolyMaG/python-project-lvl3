#!/usr/bin/env python3
import os
import sys
import logging
import argparse
from page_loader.changer import KnownError
from page_loader.loader import save_page


parser = argparse.ArgumentParser(description='page-loader')
parser.add_argument(
    '--output',
    default='.',
    help="set the directory to save to",
)
levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
parser.add_argument(
    '--loglevel',
    default='INFO',
    choices=levels,
    help="set the level of log message severity",
)
parser.add_argument('url')


def main():
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: %(message)s',
        filename=os.path.join(args.output, 'logfile.log'),
        filemode='w',
    )
    console = logging.StreamHandler()
    console.setLevel(args.loglevel)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging.info('Started')
    try:
        save_page(args.url, args.output)
        logging.info('Finished')
    except KnownError:
        sys.exit(1)


if __name__ == '__main__':
    main()
