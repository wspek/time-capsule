#!./venv/bin/python

import logging

from config import config
from resource import resources
from reporting import Report


logging.basicConfig(filename=config['logging']['outfile'], level=config['logging']['level'])


def main():
    logging.info('*** START ***')

    for cfg in config['resources']:
        resource_type = cfg.pop('type')

        report = Report(title=f'[{resource_type.capitalize()}] Download Report')

        resource_cls = resources.get(resource_type)
        resource = resource_cls(out_folder=config['out_folder'], report=report, **cfg)
        resource.download_all()

    logging.info('*** END ***')


if __name__ == '__main__':
    main()
