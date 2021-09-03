import yaml

CONFIG_FILE = 'config/config.yaml'


def load_config():
    with open(CONFIG_FILE) as f:
        config = yaml.safe_load(f.read())

    return config


config = load_config()
