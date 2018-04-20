import abc

class FileInfo:
    file_name = u""
    file_size = 0
    file_path = u""
    def __init__(self, name, size, path):
        self.file_name = name
        self.file_size = size
        self.file_path = path

class FolderInfo:
    folder_name = u""
    folder_path = u""
    def __init__(self, name, path):
        self.folder_name = name
        self.folder_path = path


class ClientBase:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def download_file(self, src, dst):
        pass

    @abc.abstractmethod
    def upload_file(self, src, dst):
        pass

    @abc.abstractmethod
    def get_file_info(self, path):
        pass

    @abc.abstractmethod
    def delete_file(self, path):
        pass

    @abc.abstractmethod
    def get_dir_content(self, dir_path):
        pass

    @abc.abstractmethod
    def create_dir(self, dir_path):
        pass