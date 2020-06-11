"""Module that defines Element"""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from base.configurations.exception import ElementNotFoundExcepiton, SiteIsDeadException, CustomException

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


    def __call__(self, multiple=False, index=None, implicitly_timeout=IMPLICITLY_TIMEOUT):
        """ Returns either a selenium webdriver object or list of selenium webdriver objects
        Raise ElementNotFoundException if element not found.
        Args:
            multiple (bool): if True - returns a list of found elements by specified locator.
            index (int): if present - returns element by index, from list of elements,
                         found by specified locator.
            implicitly_timeout (int) time to wait for driver to find element/elements by locator.
        """
        self.driver.implicitly_wait(implicitly_timeout)
        by_class_object = self.get_by_object(self.locator[0])

        if self.driver.find_elements(by_class_object, self.locator[1]):
            self.logger.info("Found list of elements by locator: '%s' ", self.locator)

            if multiple:
                if index:
                    self.logger.info("Returning element from list by index ")
                    try:
                        element = self.driver.find_elements(by_class_object, self.locator[1])[index]
                        self.logger.info("Found element with index %s in list of elements by locator : '%s' ",
                                         str(index), self.locator)
                        return element
                    except IndexError:
                        raise ElementNotFoundExcepiton(
                            "Element by index : '{}' not found in list of elements by locator : '{}'"
                            .format(str(index), self.locator))
                else:
                    self.logger.info("Returning whole list of elements by specified locator")
                    return self.driver.find_elements(by_class_object, self.locator[1])

            else:
                self.logger.info("Returning first element from the list.")
                return self.driver.find_elements(by_class_object, "%s" % self.locator[1])[0]

        else:
            if self.check_if_site_not_dead():
                raise ElementNotFoundExcepiton("No elements found by specified locator : '{}'."
                                               .format(self.locator))
            else:
                raise SiteIsDeadException('Base element not found. Site is dead.')

    def check_if_site_not_dead(self):
        """
        Check if base page container present in UI.
        :return: True - if base page container found.
        :return: False - if base page container not found.
        """
        try:
            self.driver.implicitly_wait(5)
            self.driver.find_element_by_css_selector(".main-container")
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def get_by_object(string_strategy):
        """ Return (By. + strategy) object, according to locator in Web Element instance
        """
        if 'xpath' in string_strategy.lower():
            return By.XPATH
        return By.CSS_SELECTOR

    def initialize_webelement(self, element, description=None, multiple=False, timeout=IMPLICITLY_TIMEOUT):
        """ Initialize WebElement, from Element object or locator
        if not yet initialized.
           :param element :
                - or locator of element that is of tuple type :
                      e.g. ("CSS_SELECTOR", ".locator");
                      e.g. ("XPATH", "//*[@class ='class']"
                - or instance of class Element :
                      e.g. Element(self.session, ("CSS_SELECTOR", ".locator"))
                - or WebElement, that is already initialized.

          :param description (str) - in case, if element is of tuple or of type Element,
          description should not be specified.  In case if element is of WebElement type
          - specify description of passed element.

          :param multiple (bool) if True - then return array of elements by locator
          :param timeout (int) second to wait for element to appear in DOM


        :return WebElement and it`s description.
        """
        if isinstance(element, Element):
            return element(multiple=multiple, implicitly_timeout=timeout), str(element.locator)
        if isinstance(element, tuple):
            return Element(self.session, element)(multiple=multiple, implicitly_timeout=timeout), str(element)
        if isinstance(element, WebElement):
            if description:
                return element, description
            else:
                return element, ''

        raise CustomException('Passed element is invalid')

    # @staticmethod
    # def get_element_description(element, description=None):
    #     """ return description for passed element"""
    #     el_description = ''
    #     if isinstance(element, Element):
    #         el_description = str(element.locator)
    #     if isinstance(element, tuple):
    #         el_description = str(element)
    #     if isinstance(element, WebElement):
    #         if description:
    #             el_description = description
    #     return el_description
