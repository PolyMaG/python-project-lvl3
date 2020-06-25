#!/usr/bin/env python3
import sys
import argparse
import logging
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
        level=args.loglevel,
        format='%(levelname)s: %(message)s',
    )
    logging.info('Started')
    try:
        save_page(args.url, args.output)
        logging.info('Finished')
    except KnownError:
        sys.exit(1)


if __name__ == '__main__':
    main()
