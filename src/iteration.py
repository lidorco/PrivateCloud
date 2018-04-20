import os

from src.logger import logger
from src.cloud_adapters.clientbase import FileInfo, FolderInfo
import src.config as g


def remove_first_slash(path):
    if path[0] == '\\' or path[0] == '/':
        return path[1:]
    return path


def join_ignore_slash(base, *paths):
    result = base
    for path in paths:
        result = os.path.join(result, remove_first_slash(path))
    return result


os.path.advjoin = join_ignore_slash


def get_local_path_without_prefix(prefix, local_dir_base, remote_file_path, remote_file_name):
    return os.path.advjoin(local_dir_base, remote_file_path[:-len(remote_file_name)],
                           remote_file_name[len(prefix):])


def get_remote_path_without_prefix(prefix, remote_file_path, remote_file_name):
    return os.path.advjoin(remote_file_path[:-len(remote_file_name)], remote_file_name[len(prefix):])


def create_partial_file(file_path, byte_length, partial_file_path):
    full_file = open(file_path, 'rb')
    content = full_file.read(byte_length)
    full_file.close()
    partial_file = open(partial_file_path, 'wb')
    partial_file.write(content)
    partial_file.close()


def dispatch_remote_iteration(client):
    logger.info("dispatch_remote_iteration started")
    remote_dir = client.get_dir_content('/')
    while len(remote_dir) != 0:
        current = remote_dir.pop()
        if current.__class__ == FolderInfo:
            remote_dir += client.get_dir_content(current.folder_path)
            if not os.path.exists(os.path.advjoin(g.local_cloud_path, current.folder_path)):
                os.mkdir(os.path.advjoin(g.local_cloud_path, current.folder_path))
            elif not os.path.isdir(os.path.advjoin(g.local_cloud_path, current.folder_path)):
                logger.error("dispatch_remote_iteration : remote path is folder, and on local its a file")
        else:
            if g.enable_upload and current.file_name.startswith(g.upload_prefix):
                logger.info("dispatch_remote_iteration : found file name start with upload magic,"
                            " uploading from local cloud")
                local_file = get_local_path_without_prefix(g.upload_prefix, g.local_cloud_path,
                                                           current.file_path, current.file_name)
                remote_file = get_remote_path_without_prefix(g.upload_prefix, current.file_path, current.file_name)

                if not os.path.exists(local_file):
                    logger.error("dispatch_remote_iteration : "
                                 "remote file start with prefix and there is no local file")
                client.delete_file(current.file_path)

                client.upload_file(local_file, remote_file)

            elif g.enable_download and current.file_name.startswith(g.download_prefix):
                logger.info("dispatch_remote_iteration : found file name start with download magic,"
                            " download to local cloud and leave thin version on remote cloud")
                local_path = get_local_path_without_prefix(g.download_prefix, g.local_cloud_path,
                                                           current.file_path, current.file_name)
                remote_path = get_remote_path_without_prefix(g.download_prefix, current.file_path, current.file_name)
                partial_file_path = os.path.advjoin(g.tmp_path, os.path.basename(remote_path))

                client.download_file(current.file_path, local_path)
                client.delete_file(current.file_path)
                create_partial_file(local_path, g.thin_mode_byte_length, partial_file_path)
                client.upload_file(partial_file_path, remote_path)
                os.remove(partial_file_path)

            elif not os.path.exists(os.path.advjoin(g.local_cloud_path, current.file_path)):
                logger.info("dispatch_remote_iteration : found file that only on remote cloud, downloading it")
                client.download_file(current.file_path, os.path.advjoin(g.local_cloud_path, current.file_path))
