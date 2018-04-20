import json
from src.logger import init_logger, logger
from src.cloud_adapters.dropbox_adapter import DropboxClient

CONFIGURATION_FILE = 'config/config.json'
DEFAULT_ACCESS_TOCKEN = 'YOUR_ACCESS_TOKEN'

dropbox_client = None

local_cloud_path = ""
upload_prefix = ""
enable_upload = False
download_prefix = ""
enable_download = False
thin_mode_byte_length = 0
tmp_path = ""
sync_interval_in_sec = 1

def load_configuration():
    global dropbox_client, local_cloud_path, upload_prefix, enable_upload, download_prefix, enable_download, \
        thin_mode_byte_length, tmp_path, sync_interval_in_sec
    file_handle = open(CONFIGURATION_FILE, 'r')
    config_data = file_handle.read()
    file_handle.close()
    configs = json.loads(config_data)
    
    init_logger(configs["server_configuration"]["log_path"])

    local_cloud_path = configs["server_configuration"]["local_cloud_path"]
    upload_prefix = configs["server_configuration"]["upload_filename_magic"]
    download_prefix = configs["server_configuration"]["download_filename_magic"]
    enable_download = bool(configs["server_configuration"]["enable_download"])
    enable_upload = bool(configs["server_configuration"]["enable_upload"])
    thin_mode_byte_length = int(configs["server_configuration"]["bytes_length_in_thin_mode"])
    tmp_path = configs["server_configuration"]["tmp_path"]
    sync_interval_in_sec = configs["server_configuration"]["sync_interval_in_sec"]

    if configs["cloud_credential"]["dropbox"]["access_token"] is not DEFAULT_ACCESS_TOCKEN:
        dropbox_client = DropboxClient(configs["cloud_credential"]["dropbox"]["access_token"])

    logger.info("Finish loading configuration")
