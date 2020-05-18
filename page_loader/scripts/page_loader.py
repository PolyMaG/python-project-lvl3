#!/usr/bin/env python3
import argparse
from page_loader.loader import get_page


parser = argparse.ArgumentParser(description='page-loader')
parser.add_argument(
    '--output',
    default='.',
    help="set the directory to save to",
)
parser.add_argument('source')


def main():
    args = parser.parse_args()
    saved_page_path = get_page(args.source, args.output)
    return saved_page_path


if __name__ == '__main__':
    main()
