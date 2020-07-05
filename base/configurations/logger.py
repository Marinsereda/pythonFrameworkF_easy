"""LOGGER MODULE"""
import logging

class Logger:
    """
    Class Logger
    """
    def __init__(self, name):
        """
        Creating logger with file name specified
        at the top level
        """
        LOGGER = logging.getLogger(name)
        LOGGER.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        LOGGER.addHandler(handler)
        self.logger = LOGGER
