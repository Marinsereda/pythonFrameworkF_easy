"""Module that defines Element"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from base.configurations.exception import ElementNotFoundExcepiton, CustomException

IMPLICITLY_TIMEOUT = 60


class Element:
    """Class describes Element class.
    """

    def __init__(self, session, locator=None):
        """
        Initialize object of class Element.
        :param session (obj) - instance of the session class
        :param locator of element that is of tuple type :
                      e.g. ("CSS_SELECTOR", ".locator");
                      e.g. ("XPATH", "//*[@class ='class']"
        """
        self.session = session
        self.locator = locator
        self.driver = session.driver
        self.logger = session.logger


    def __call__(self, multiple=False, implicitly_timeout=IMPLICITLY_TIMEOUT):
        """ Returns either a selenium webdriver object or list of selenium webdriver objects
        Raise ElementNotFoundException if element not found.
        Args:
            multiple (bool): if True - returns a list of found elements by specified locator.
            implicitly_timeout (int) time to wait for driver to find element/elements by locator.
        """
        self.driver.implicitly_wait(implicitly_timeout)
        by_class_object = self.get_by_object(self.locator[0])

        if multiple:
            return self.driver.find_elements(by_class_object, self.locator[1])
        else:
            if not self.driver.find_elements(by_class_object, self.locator[1]):
                raise ElementNotFoundExcepiton(
                    "Element by locator : '{}' not found. Waited for : '{} seconds'"
                    .format(self.locator, implicitly_timeout))
            else:
                return self.driver.find_elements(by_class_object, self.locator[1])[0]

    @staticmethod
    def get_by_object(string_strategy):
        """ Return (By. + strategy) object, according to locator in Web Element instance
        """
        if 'xpath' in string_strategy.lower():
            return By.XPATH
        return By.CSS_SELECTOR

    def initialize_webelement(self, element, description='', multiple=False, timeout=IMPLICITLY_TIMEOUT):
        """ Initialize WebElement, from Element object or locator
        if not yet initialized.
           :param element :
                - or locator of element that is of tuple type :
                      e.g. ("CSS_SELECTOR", ".locator");
                      e.g. ("XPATH", "//*[@class ='class']"
                - or instance of class Element :
                      e.g. Element(self.session, ("CSS_SELECTOR", ".locator"))
                - or WebElement, that is already initialized.

          :param description (str) - optional param. Prefered to specify description for
           already found Elements.  (Webelement type)


          :param multiple (bool) if True - then return array of elements by locator
          :param timeout (int) second to wait for element to appear in DOM


        :return WebElement and it`s description.
        """
        if isinstance(element, Element):
            return element(multiple=multiple, implicitly_timeout=timeout), str(element.locator)
        if isinstance(element, tuple):
            return Element(self.session, element)(multiple=multiple, implicitly_timeout=timeout), str(element)
        if isinstance(element, WebElement):
            return element, description

        raise CustomException('Passed element is invalid')
