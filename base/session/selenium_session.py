"""SELENIUM SESSION MODULE"""

from base.driver.driver import Driver


class SeleniumSession:
    """Defining selenium session"""
    ip = None
    profile = None
    binary = None

    def __init__(self, config, logger, browser="chrome"):
        """
        Start selenium session:
        :param args:
        :param browser: type browser
        :param local: open local browser
        :param local_zalenium: if local_zalenium flag True: Open zalenium in local docker
        :param logger:
        :param kwargs:
        """
        self.logger = logger
        self.driver = Driver(browser, logger).driver
        self.session_id = self.driver.session_id
        self.credentials = (config.get("ISE", "USERNAME"),
                            config.get("ISE", "PASSWORD"))

    # @staticmethod
    # def get_value_from_config_object(key, config_object=DEFAULT_CONFIG):
    #     """get config object"""
    #     return config_object[key]
