"""
Describes all wait methods.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from base.configurations.exception import *
from base.configurations.element import Element


TIMEOUT = 30
POLL_FREQUENCY = 0.5


class Waits:
    """ Class describes selenium waits methods.

    Commonly used parameters:
    :param element :
    - or locator of element that is of tuple type :
          e.g. ("CSS_SELECTOR", ".locator");
          e.g. ("XPATH", "//*[@class ='class']"
    - or instance of class Element :
          e.g. Element(self.session, ("CSS_SELECTOR", ".locator"))
    - or WebElement, that is already initialized.
     :param el_description (str) - In case if element is of WebElement type
            - specify description of passed element.


    """
    def __init__(self, session):
        """
         :param session (obj) - instance of the session class
        """
        self.session = session
        self.logger = session.logger
        self.driver = session.driver

    def wait_for_web_element_visible(self, element, el_description='',
                                     timeout=TIMEOUT,  poll_frequency=POLL_FREQUENCY,
                                     raise_exception=True):
        """ An expectation for checking that the element is present in the DOM and
            is visible.
            :param element : watch in description to this module
            :param el_description (str) description of the element
            :param timeout: (int): time to wait for condition
            poll_frequency (float): sleep interval between calls
            raise_exception (bool): whether to raise an exception when expected condition not met
            or not.
        Returns: True - if element is present and visible. Returns false - if element is invisible
        and raise_exception is False.
        """
        try:
            web_element, el_description = Element(self.session).initialize_webelement(element, el_description, timeout=timeout)
            self.logger.info("Waiting for following element to be displayed : '%s'" % el_description)
            return WebDriverWait(self.driver, timeout, poll_frequency).until(ec.visibility_of(web_element))
        except (ElementNotFoundExcepiton, NoSuchElementException) as element_not_found_e:
            if raise_exception:
                raise element_not_found_e
            else:
                self.logger.info("WebElement '%s' is not present in DOM. Waited for '%s' seconds." % (el_description, timeout))

        except TimeoutException:
            if raise_exception:
                raise ElementNotVisibleExcepiton(
                    "WebElement '%s' is not visible in DOM. Waited for '%s' seconds." % (el_description, timeout))

        return False

    def wait_for_web_element_not_visible(self, element, el_description='', timeout=TIMEOUT,
                                         poll_frequency=POLL_FREQUENCY, raise_exception=False):
        """ An expectation for checking that the WebElement is not present in the DOM or is invisible.
        (not displayed/ hidden)
        :param element : watch in description to this module
        :param el_description (str) description of the elementWebElement type
                - specify description of passed element.
        :param timeout: (int): time to wait for condition
        poll_frequency (float): sleep interval between calls
        raise_exception (bool): whether to raise an exception when expected condition not met
        or not.
        Returns:
            obj: WebElement once it is located and then become invisible
            bool: False if the WebElement not became invisible, or disappear from DOM, after specified time out.
        """
        try:
            self.logger.info("Waiting for webelement {} to be no longer visible or present".format(el_description))
            web_element, el_description = Element(self.session).initialize_webelement(element, el_description, timeout=1)
            return WebDriverWait(self.driver, timeout, poll_frequency).until(ec.invisibility_of_element_located(web_element))
        except TimeoutException:
            if raise_exception:
                raise FlowFailedException(
                    "WebElement '%s' is still visible. Waited element not to be visible for '%s' seconds."
                    % (el_description, timeout))
            return False

        except ElementNotFoundExcepiton:
            return True

    def wait_for_element_to_be_enabled(self, element, el_description='',
                                     timeout=TIMEOUT,  poll_frequency=POLL_FREQUENCY,
                                     raise_exception=True):
        """An expectation for checking that the WebElement is enabled and available for interaction.
            :param element : watch in description to this module
            :param el_description (str) description of the element
            :param timeout: (int): time to wait for condition
            :param poll_frequency: (float) sleep interval between calls
            param: raise_exception (bool): whether to raise an exception when expected condition
            not met or not.
        Returns:
            WebElement once it is clickable
            bool: False if WebElement is not clickable and raise_exception is False
        """
        web_element, el_description = Element(self.session).initialize_webelement(element, el_description)
        self.logger.info("Waiting for following element to be enabled : '%s'", el_description)
        try:
            return WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda element_enabled: web_element.is_enabled())
        except TimeoutException:
            if raise_exception:
                raise ElementIsDisabledException("Element '%s' is disabled. Waited for '%s' seconds."
                                                 .format(el_description, timeout))
            return False

    def wait_for_web_element_attribute_to_contain(self, element, text, el_description='', attribute='value',
                                                  timeout=TIMEOUT, raise_exception=True):
        """ An expectation for checking if the given string is present in webelement's attribute
        Args:
            :param element : watch in description to this module
            :param el_description (str) description of the element
            :param text - (str) specified text, excepted to be present in elements attribute
            :param timeout: (int): time to wait for condition
            param: raise_exception (bool): whether to raise an exception when expected condition
            not met or not.
            :param attribute: (str): attribute of element
            :param timeout: (int): time to wait
        Returns:
            bool: True if the text present in the element's attribute
            bool: False if not present in the element's attribute and raise_exception is False
        """
        web_element, el_description = Element(self.session).initialize_webelement(element, el_description)
        poll_frequency = 0.5
        self.logger.info("Waiting for '{0}' string to be present in attribute '{1}' of element '{2}'"
                         .format(text, attribute, el_description))
        try:
            return WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda element_attribute: text in web_element.get_attribute(attribute))
        except TimeoutException:
            if raise_exception:
                raise FlowFailedException(
                    "'{0}' not appeared in attribute '{1}' of WebElement '{2}'."
                    "Waited for '{3}' seconds.".format(text, attribute, el_description, timeout))
            else:
                return False

    def wait_for_web_element_attribute_not_to_contain(self, element, text, el_description='', attribute='value',
                                                  timeout=TIMEOUT, raise_exception=True):
        """ An expectation for checking if the given string is not present in webelement's attribute
        Args:
            :param element : watch in description to this module
            :param el_description (str) description of the element
            :param text - (str) specified text, excepted to be present in elements attribute
            :param timeout: (int): time to wait for condition
            param: raise_exception (bool): whether to raise an exception when expected condition
            not met or not.
            :param attribute: (str): attribute of element
            :param timeout: (int): time to wait
        Returns:
            bool: True if the text present in the element's attribute
            bool: False if not present in the element's attribute and raise_exception is False
        Raises:
            FlowFailedException: When condition is not met and raise_exception is True
        """
        web_element, el_description = Element(self.session).initialize_webelement(element, el_description)
        poll_frequency = 0.5
        self.logger.info("Waiting for '{0}' to be no longer present in attribute '{1}' of element '{2}'"
                         .format(text, attribute, el_description))
        try:
            return WebDriverWait(self.driver, timeout, poll_frequency).until(
                lambda element_attribute: text not in web_element.get_attribute(attribute))
        except TimeoutException:
            if raise_exception:
                raise FlowFailedException(
                    "Text '{0}' is still present in attribute of  '{1}' of WebElement '{2}'."
                    "Waited for '{3}' seconds.".format(text, attribute, el_description, timeout))


    def wait_for_text_to_be_present_in_element(self, element, text, el_description='', timeout=TIMEOUT,
                                                   raise_exception=True):
        """ An expectation for checking if the given text is
        present in the specified element.
        Similar to checking if text not in ".text" method called on a webelement
        Args:
            :param element : watch in description to this module
            :param el_description (str) description of the element
            :param text - (str) specified text, excepted to be present in element
            :param timeout: (int): time to wait for condition
            param: raise_exception (bool): whether to raise an exception when expected condition
            not met or not.
        Returns:
            bool: True if the text present in the element's inner text
            bool: False if not present and raise_exception is False
        """
        web_element, el_description = Element(self.session).initialize_webelement(element, el_description)
        self.logger.info("Waiting for text: {0} to be present in element: {1}".format(
            text, el_description))
        try:
            return WebDriverWait(self.driver, timeout).until(
                lambda element_text: text in web_element.text)
        except TimeoutException:
            if raise_exception:
                raise FlowFailedException(
                    "Text '{0}' is not present in Element '{1}'. "
                    "Waited for '{2}' seconds.".format(text, el_description, timeout))
            else:
                return False

    def wait_for_text_not_to_be_present_in_element(self, element, text, el_description='', timeout=TIMEOUT,
                                                   raise_exception=True):
        """ An expectation for checking if the given text is
        present in the specified element.
        Similar to checking if text not in ".text" method called on a webelement
        Args:
            :param element : watch in description to this module
            :param el_description (str) description of the element
            :param text - (str) specified text, excepted to be not longer present in element
            :param timeout: (int): time to wait for condition
            param: raise_exception (bool): whether to raise an exception when expected condition
            not met or not.
        Returns:
            bool: True if the text not present in the element's inner text
            bool: False if still present and raise_exception is False
        Raises:
            FlowFailedException: When condition is not met and raise_exception is True
        """
        web_element, el_description = Element(self.session).initialize_webelement(element, el_description)
        self.logger.info("Waiting for text: {0} to be no longer present in element: {1}".format(
            text, el_description))
        try:
            return WebDriverWait(self.driver, timeout).until(
                lambda element_text: text not in web_element.text)
        except TimeoutException:
            if raise_exception:
                raise FlowFailedException(
                    "Text '{0}' is still present in Element '{1}'. Waited for '{2}' seconds.".format(text, el_description, timeout))
            else:
                return False

    def wait_for_number_of_elements_present(self, element, el_description='', expected_number=1, precisely=False,
                                            timeout=TIMEOUT, raise_exception=True):
        """ An expectation for checking quantity of elements in DOM >= expected quantity.
        Args:
            :param element : watch in description to this module
            :param el_description (str) description of the element
            :param expected_number: (int): quantity of elements expected to be present in DOM
            timeout (int): time to wait
            poll_frequency (float): sleep interval between calls
            raise_exception (bool): whether or not to raise an exception or return False
        Returns:
            bool: True if condition met
            bool: False if condition not met and raise_exception is False
        """
        web_elements, el_description = Element(self.session).initialize_webelement(element, el_description, multiple=True)
        self.logger.info("Waiting for number of present elements by locator '{}'  >= expected number : '{}'"
                         .format(el_description,  expected_number))

        try:
            return WebDriverWait(self.driver, timeout).until(lambda length: len(web_elements) >= expected_number)

        except TimeoutException:
            if raise_exception:
                raise FlowFailedException("Number of webelements by locator '{}' present in DOM is : '{}'. "
                                          "Expected number of elements to be present is '{}'. Waited for '{}' seconds."
                                          .format(el_description, len(web_elements), expected_number, timeout))
            else:
                return False

    def wait_for_alert_is_present(self, timeout=TIMEOUT, poll_frequency=POLL_FREQUENCY,
                                  raise_exception=True):
        """ An expectation for an alert to be present.
        Args:
            timeout (int): time to wait
            poll_frequency (float): sleep interval between calls
            raise_exception (bool): whether or not to raise an exception or return False
        Returns:
            bool: True alert if present
            bool: False if alert is absent and raise_exception is False
        Raises:
            ElementNotFoundException: When condition is not met and raise_exception is True
        """
        self.logger.info("Waiting for alert to be present")
        try:
            return WebDriverWait(self.driver, timeout, poll_frequency).until(ec.alert_is_present())
        except TimeoutException:
            if raise_exception:
                raise FlowFailedException("Alert is not present. Waited for '{0}' seconds."
                                          .format(timeout))
            return False
