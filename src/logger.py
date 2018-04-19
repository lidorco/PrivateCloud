import logging


logger = logging.getLogger('privatecloud')
hdlr = logging.FileHandler('privatecloud.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
