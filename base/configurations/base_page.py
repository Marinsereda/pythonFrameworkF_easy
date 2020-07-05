
import time
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
from selenium.webdriver.remote.webelement import WebElement
from base.configurations.interactions import Interactions
from base.configurations.waits import Waits

from base.configurations.element import Element
# from iseac.base.selenium.pages.utils import get_merged_page_config

class BasePage:

    def __init__(self, session, make_login=True):
        self.session = session
        self.driver = session.driver
        self.logger = session.logger
        self.action = Interactions(self.session)
        self.waits = Waits(self.session)
        if make_login:
            self.login_to_booking()
