"""ISEAC BASE MODULE"""
import time
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
from selenium.webdriver.remote.webelement import WebElement
from base.configurations.interactions import Interactions
from base.configurations.waits import Waits
from base.configurations.element import Element
# from iseac.base.selenium.pages.utils import get_merged_page_config

class BasePage(Element):

    """ Base Framework Class. This class is the main (super parent) for all framework classes.
    It sets all base dependencies and contains base methods."""

    def __init__(self, session):
        """ Set all locators provided in the Page config file (config.ELEMENTS dict)
       as class attributes, and run all the validations on page/form loaded, based
       on locators in page config file (config.VALIDATIONS list)
        :param session (obj) - instance of the session class
       :param config: specified page config
       """
        self.session = session
        self.driver = session.driver
        self.logger = session.logger
        self.action = Interactions(self.session)
        self.waits = Waits(self.session)
