import time

from src.config import load_configuration
from src.logger import logger
from iteration import dispatch_remote_iteration, dispatch_local_iteration
import src.config as g


def main():
    load_configuration()
    logger.info("Private Cloud started")

    while True:
        try:
            dispatch_remote_iteration(g.dropbox_client)
            dispatch_local_iteration(g.dropbox_client)
            logger.info("Finish iteration. sleeping...")
            time.sleep(g.sync_interval_in_sec)
        except Exception as e:
            logger.error("Exception occurred: {0}".format(str(e)))


if __name__ == '__main__':
    main()
