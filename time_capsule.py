#!./venv/bin/python

import logging

from config import config
from resource import resources

logging.basicConfig(filename=config['logging']['outfile'], level=config['logging']['level'])


def main():
    logging.info('*** START ***')

    for cfg in config['resources']:
        resource_type = cfg.pop('type')
        resource = resources.get(resource_type)(out_folder=config['out_folder'], **cfg)
        resource.download_all()

    logging.info('*** END ***')


if __name__ == '__main__':
    main()
