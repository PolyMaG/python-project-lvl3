#!/usr/bin/env python3
import argparse
from page_loader.loader import save_page


parser = argparse.ArgumentParser(description='page-loader')
parser.add_argument(
    '--output',
    default='.',
    help="set the directory to save to",
)
parser.add_argument('url')


def main():
    args = parser.parse_args()
    save_page(args.url, args.output)


if __name__ == '__main__':
    main()
