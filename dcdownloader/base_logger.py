import logging
from colorlog import ColoredFormatter

logging_level = logging.INFO

def getLogger(name=__name__):
    logger_base = logging.getLogger(name)
    logger_base.setLevel(logging_level)
    stream_handler = logging.StreamHandler()

    color_formatter = ColoredFormatter('%(log_color)s[%(levelname)-8s] %(message)s')
    
    stream_handler.setFormatter(color_formatter)

    logger_base .addHandler(stream_handler)
    

    return logger_base 