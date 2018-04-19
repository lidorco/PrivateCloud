import json
from src.logger import init_logger, logger
from src.cloud_adapters.dropbox_adapter import DropboxClient

CONFIGURATION_FILE = 'config/config.json'
DEFAULT_ACCESS_TOCKEN = 'YOUR_ACCESS_TOKEN'

local_cloud_path = ""
dropbox_client = None

def load_configuration():
    global dropbox_client, local_cloud_path
    file_handle = open(CONFIGURATION_FILE, 'r')
    config_data = file_handle.read()
    file_handle.close()
    configs = json.loads(config_data)
    
    init_logger(configs["server_configuration"]["log_path"])

    local_cloud_path = configs["server_configuration"]["local_cloud_path"]

    if configs["cloud_credential"]["dropbox"]["access_token"] is not DEFAULT_ACCESS_TOCKEN:
        dropbox_client = DropboxClient(configs["cloud_credential"]["dropbox"]["access_token"])

    logger.info("Finish loading configuration")
