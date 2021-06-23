import yaml

config = "./config/config.yml"


def load(cfg=config):
    with open(cfg, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None
