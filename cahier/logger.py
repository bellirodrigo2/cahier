""" Logger """
import logging.config
import pathlib
import json
################################################################################

def setup_logging():
    config_file = pathlib.Path('./logger.json')
    with open(config_file) as f:
        config = json.load(f)
    logging.config.dictConfig(config)

def get_logger(name: str):
    setup_logging()
    return logging.getLogger(name)
    

if __name__ == '__main__':

    logger = get_logger('cahi')
    logger.debug('debdsp ')
    logger.error('oekfofke')