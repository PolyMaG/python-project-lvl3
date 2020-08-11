#!/usr/bin/env python3
import logging
import sys

from progress.bar import IncrementalBar

from page_loader.configs import parser, set_logging
from page_loader.helpers import KnownError
from page_loader.loader import save_page


def main():
    args = parser(sys.argv[1:]).parse_args()
    set_logging()
    logging.info('Started.\n')
    try:
        with IncrementalBar('Page saving', max=10) as bar:
            for item in range(10):
                bar.next()
        save_page(args.url, args.output)
    except KnownError:
        logging.error('Program has stopped.')
        sys.exit(1)
    else:
        logging.info('\nFinished.')


if __name__ == '__main__':
    main()
