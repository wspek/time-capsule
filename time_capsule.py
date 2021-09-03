#!./venv/bin/python

import logging

from config import config
from resources import Resource

logging.basicConfig(filename=config['logging']['outfile'], level=config['logging']['level'])


def main():
    logging.info('*** START ***')

    # Iterate over config
    for cfg in config['resources']:
        resource = Resource.create(folder=config['folder'], **cfg)
        resource.download()

    logging.info('*** END ***')


if __name__ == '__main__':
    main()
