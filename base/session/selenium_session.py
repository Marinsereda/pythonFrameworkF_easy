import configparser
import os
from base.driver.driver import Driver
path_to_default_config = (os.path.dirname(os.path.realpath(__file__)) + "/../configs/default_config.ini")
DEFAULT_CONFIG = configparser.ConfigParser()
DEFAULT_CONFIG.read(path_to_default_config)


class SeleniumSession:

    def __init__(self, logger, browser='chrome', url=None, credentials=None):
        """
        Setting attributes for selenium session:
        """
        logger.info("Initializing selenium session...")
        self.logger = logger

        # open browser
        self.driver = Driver(browser, self.logger).driver

        # set credentials
        if not credentials:
            self.credentials = (DEFAULT_CONFIG.get("TEST CONFIG", "USERNAME"),
                                DEFAULT_CONFIG.get("TEST CONFIG", "PASSWORD"))
        else:
            self.credentials = credentials

        # set URL
        if not url:
            self.url = DEFAULT_CONFIG.get("TEST CONFIG", "URL")
        else:
            self.url = url
