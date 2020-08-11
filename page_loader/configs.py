import argparse
import logging
import os
import sys

LOG_FORMAT = '%(levelname)s: %(message)s'


def parser(*args):
    """Define arguments for parsing cli-inputs."""
    parser = argparse.ArgumentParser(description='page-loader')
    parser.add_argument(
        '-o',
        '--output',
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


def set_logging():
    """Define logging settings."""
    args = parser(sys.argv[1:]).parse_args()
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FORMAT,
        filename=os.path.join(args.output, 'logfile.log'),
        filemode='w',
    )
    console = logging.StreamHandler()
    console.setLevel(args.loglevel)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
