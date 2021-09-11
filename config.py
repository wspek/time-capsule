import yaml
import pathlib

CONFIG_FILE = f'{pathlib.Path(__file__).parent.resolve()}/config/config.yaml'


def load_config():
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f.read())

    return config


config = load_config()
