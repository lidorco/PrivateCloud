import dropbox

from src.cloud_adapters.clientbase import ClientBase, FileInfo, FolderInfo
from src.logger import logger


class DropboxClient(ClientBase):

    def __init__(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)
        try:
            info = self.dbx.users_get_current_account()
            logger.info("DROPBOX : Connect to user {0}".format(info.name.display_name))
        except Exception as e:
            logger.info("DROPBOX : Failed to connect dropbox!")
            raise e

    def download_file(self, src, dst):
        response = self.dbx.files_download(src)
        local_file = open(dst, 'wb')
        data = response[1].content
        local_file.write(data)
        local_file.close()

    def upload_file(self, src, dst):
        local_file = open(src, 'rb')
        content = local_file.read()
        local_file.close()
        self.dbx.files_upload(content, dst, mute=True)

    def get_file_info(self, path):
        response_info = self.dbx.files_get_metadata(path)
        return FileInfo(response_info.name, response_info.size, response_info.path_display)

    def delete_file(self, path):
        self.dbx.files_delete_v2(path)

    def get_dir_content(self, dir_path):
        if dir_path == "/":
            dir_path = ""
        response = self.dbx.files_list_folder(dir_path)
        entries = []
        for entry in response.entries:
            if type(entry) == dropbox.files.FolderMetadata:
                entries.append(FolderInfo(entry.name, entry.path_display))
            elif type(entry) == dropbox.files.FileMetadata:
                entries.append(FileInfo(entry.name, entry.size, entry.path_display))
            else:
                logger.error("DROPBOX : Unknown entry in dir {0}".format(dir_path))

        while response.has_more:
            response = self.dbx.files_list_folder_continue(response.cursor)
            for entry in response.entries:
                if type(entry) == dropbox.files.FolderMetadata:
                    entries.append(FolderInfo(entry.name, entry.path_display))
                elif type(entry) == dropbox.files.FileMetadata:
                    entries.append(FileInfo(entry.name, entry.size, entry.path_display))
                else:
                    logger.error("DROPBOX : Unknown entry in dir {0}".format(dir_path))

        return entries

    def create_dir(self, dir_path):
        self.dbx.files_create_folder_v2(dir_path)
