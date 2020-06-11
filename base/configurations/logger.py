"""LOGGER MODULE"""
import logging

# class Logger:
#     def __init__(self):
#         LOGGER = logging.getLogger( __name__)
#         LOGGER.setLevel(logging.DEBUG)
#         # Create handlers
#         HANDLER = logging.StreamHandler()
#
#         # Create formatters
#         FORMAT = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
#         HANDLER.setFormatter(FORMAT)
#
#         # Add handlers to the logger
#         LOGGER.addHandler(HANDLER)
#
#         self.logger = LOGGER
#         self.logger.info('Logger instance started ')

class Logger:
    """
    Class Logger
    """
    def __init__(self, name):
        """
        Creating logger with file name specified
        at the top level
        """
        # LOGGER = logging.getLogger(__name__)
        LOGGER = logging.getLogger(name)
        LOGGER.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        LOGGER.addHandler(handler)
        self.logger = LOGGER

    # @staticmethod
    # def create_logger(name):
    #     """
    #     Creating logger with file name specified
    #     at the top level
    #     """
    #     logger = logging.getLogger(name)
    #     logger.setLevel(logging.DEBUG)
    #     handler = logging.StreamHandler()
    #     logger.addHandler(handler)
    #     return logger
