"""Module that describes driver"""
from selenium import webdriver
from base.driver import driver_config
# from base.configurations.logger import Logger

# LOGGER = Logger.create_logger(__name__)
# LOGGER = Logger(__name__).logger


class Driver:
    """
    Class which represents selenium web driver
    """

    def __init__(self, browser, logger):
        """
        :param (str) browser: browser type (e.g "Chrome")
        :param args:
        :param kwargs:
        """
        self.logger = logger
        self.init_driver(browser.lower())

    def init_driver(self, browser):
        """_"""
        if 'chrome' in browser:
            self.driver = webdriver.Chrome(
                executable_path=driver_config.CONFIG[browser]['path_to_driver'],
                desired_capabilities=driver_config.CONFIG[browser]['settings'])
        elif 'firefox' in browser:
            self.driver = webdriver.Firefox(
                executable_path=driver_config.CONFIG[browser]['path_to_driver'],
                desired_capabilities=driver_config.CONFIG[browser]['settings'])

        self.driver.maximize_window()
        # self.session_id = self.driver.session_id
        self.logger.info("Selenium web driver was initialized")
        # return self.driver
