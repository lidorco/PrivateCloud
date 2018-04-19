import json
from src.logger import init_logger, logger


CONFIGURATION_FILE = 'config/config.json'

def load_configuration():
    file_handle = open(CONFIGURATION_FILE, 'r')
    config_data = file_handle.read()
    file_handle.close()
    configs = json.loads(config_data)
    
    init_logger(configs["server_configuration"]["log_path"])
