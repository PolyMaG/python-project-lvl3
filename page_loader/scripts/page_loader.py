#!/usr/bin/env python3
import argparse
import logging
from page_loader.loader import save_page


parser = argparse.ArgumentParser(description='page-loader')
parser.add_argument(
    '--output',
    default='.',
    help="set the directory to save to",
)
levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
parser.add_argument(
    '--log',
    default='INFO',
    choices=levels,
    help="set the level of log message severity",
)
parser.add_argument('url')


def main():
    args = parser.parse_args()
    logging.basicConfig(
        level=args.log,
        format='%(levelname)s: %(message)s',
    )
    logging.info('Started')
    save_page(args.url, args.output)
    logging.info('Finished')


if __name__ == '__main__':
    main()
