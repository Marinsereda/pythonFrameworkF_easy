"""Interactions module. (Defining actions, that can be executed with elements
Common arguments, present in class methods of this module:

:param element :
                - or locator of element that is of tuple type :
                      e.g. ("CSS_SELECTOR", ".locator");
                      e.g. ("XPATH", "//*[@class ='class']"
                - or instance of class Element :
                      e.g. Element(self.session, ("CSS_SELECTOR", ".locator"))
                - or WebElement, that is already initialized.
:param el_description (str) - In case if element is of WebElement type - specify description of passed element.
                              If element is of tuple type or of Element type - no description needed to specify.

"""
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from base.configurations.element import Element
from base.configurations.waits import Waits
from base.configurations.exception import *

IMPLICITLY_TIMEOUT = 60

class Interactions:
    """ Class that describes interaction with elements.
    """

    def __init__(self, session):
        self.driver = session.driver
        self.waits = Waits(session)
        self.logger = session.logger
        self.initialize_webelement = Element.initialize_webelement

    # Get info about element

    def is_elements_present(self, element, timeout=5):
        """Check if element is present.
        :param element :  - or locator of element that is of tuple type :
                      e.g. ("CSS_SELECTOR", ".locator");
                      e.g. ("XPATH", "//*[@class ='class']"
                      -   or instance of class Element :
                      e.g. Element(self.session, ("CSS_SELECTOR", ".locator"))
        :param el_description (str) description of the element
        :param timeout (int) time to wait for element is displayed
        """
        try:
            self.logger.info("Start checking if element present {}".format(element))
            self.initialize_webelement(element,  timeout=timeout)
            self.logger.info('Found following element: {}'.format(element))
            return True
        except ElementNotFoundExcepiton:
            self.logger.info('Element by locator "{}" not found. Waited for  "{}"'.format(element, timeout))
            return False

    def is_element_displayed(self, element, el_description='', timeout=5):
        """return element is_displayed status by selenium operator.
        :param element : watch in description to this module
        :param el_description (str) description of the element
        :param timeout (int) time to wait for element is displayed
        """
        try:
            web_element, description = self.initialize_webelement(element, el_description, timeout=timeout)
            self.logger.info("Start checking if element '{}' is displayed".format(description))
            if web_element.is_displayed():
                self.logger.info('Element by locator "{}" is displayed.'.format(description))
                return True
            else:
                self.logger.info('Element by locator "{}" is not displayed (visible).'.format(description))
                return False

        except ElementNotFoundExcepiton:
            self.logger.info('Element by locator "{}" not found. Waited for  "{}"'.format(description, timeout))

            return False

    def is_element_selected(self, element, el_description=''):
        """return element is_checked status by selenium operator.
        :param element : watch in description to this module
        :param el_description (str) description of the element
        """
        web_element, description = self.initialize_webelement(element, el_description)
        self.logger.info("Start checking if element '{}' is selected".format(description))
        try:
            return web_element.is_selected()
        except Exception as exception:
            raise ElementNotAvailableException(
                "Failed to get selected/unselected status of following element : '{}' "
                "due to following exception: '{}'".format(description, str(exception)))

    # Getters:

    def get_text(self, element, el_description=''):
        """get inner text of element
        :param element : watch in description to this module
        :param el_description (str) description of the element

        """
        web_element, description = self.initialize_webelement(element, el_description)
        self.logger.info("Getting text from element '{}'".format(description))
        self.waits.wait_for_web_element_visible(element)
        try:
            return web_element.text.strip()
        except Exception as exception:
            raise ElementNotAvailableException("Can't get text from following element '{}'. Got following error: '{}'"
                                               .format(description, str(exception)))

    def get_attribute(self, element, el_description='', attribute='value'):
        """get specified attribute from element
         :param element : watch in description to this module
        :param el_description (str) description of the element
        """
        web_element, description = self.initialize_webelement(element, el_description)
        self.logger.info("Getting attribute: '{}' from element '{}'".format(attribute, el_description))
        try:
            return web_element.get_attribute(attribute).lower()
        except NoSuchAttributeException:
            raise AttributeNotFoundException("Following element: '{}' has no attribute '{}'"
                                             .format(description, attribute))

    # Scrolls:

    def scroll_in_to_view(self, element, el_description=''):
        """ Scroll into the view of the element.
        :param element : watch in description to this module
        :param el_description (str) description of the element
        """
        web_element, description = self.initialize_webelement(element, el_description)
        self.logger.info("Scrolling in to view of Element '{}'".format(description))
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", web_element)
        except Exception as e:
            raise CustomException('Failed to scroll to element "{}". Got following exception "{}"'
                                  .format(description, str(e)))

    def scroll_to_top(self):
        """
        Scrolling to top of page
        """
        self.logger.info("Scrolling to top")
        self.driver.execute_script("window.scrollTo(0, 0)")

    def scroll_to_bottom(self):
        """
        Scrolling to bottom of page
        """
        self.logger.info("Scrolling to bottom")
        self.driver.execute_script("window.scrollTo(0, 2000)")

    # Click

    def click(self, element, el_description='', wait_to_be_enabled=True):
        """perform click on element
        :param element :  - or locator of element that is of tuple type :
                      e.g. ("CSS_SELECTOR", ".locator");
                      e.g. ("XPATH", "//*[@class ='class']"
                      -   or instance of class Element :
                      e.g. Element(self.session, ("CSS_SELECTOR", ".locator"))
       :param el_description (str) description of the element
       :param wait_to_be_enabled: (bool) if true - then wait for element to be enabled before entering keys.
        """
        web_element, description = self.initialize_webelement(element, el_description)
        self.logger.info("Clicking on following element '{}'".format(description))

        if wait_to_be_enabled:
            self.waits.wait_for_element_to_be_enabled(element, el_description)
        try:
            self.logger.info("Clicking on following element '{}'".format(description))
            web_element.click()

        except Exception as exception:

            if not web_element.is_enabled():
                raise ElementIsDisabledException('Following element "{}" is disabled. '.format(description))

            raise ElementNotAvailableException(
                'Failed to click to following elelement: "{}". Got following errror: "{}".'
                .format(description, str(exception)))

    def click_element_with_js(self, element, el_description=''):
        """
        Executes click action using
        Javascript
        """
        web_element, description = self.initialize_webelement(element, el_description)
        self.logger.info("Clicking on following element with JS : '{}'".format(description))
        try:
            self.driver.execute_script("return arguments[0].click()", web_element)
        except Exception as e:
            raise UnExpectedException('Failed to click to following element with JS : "{}"'.format(description))

    # Hover / drug and drop


    def hover(self, element, el_description=''):
        """ Performs a mouseover/hover on element
        Moves mouse to the middle of the element
        Args:
            xoffset (int): offset from upper left to click on element
            yoffset (int): offset from upper left to click on element
        """
        web_element, description = self.initialize_webelement(element, el_description)
        self.logger.info("Hovering on following element '{}'".format(description))
        action_chains = ActionChains(self.driver)
        try:
            action_chains.move_to_element(web_element).perform()

        except Exception as caught_exception:
            raise CustomException(
                    'Failed to hover on element: "{}", Caught following exception: "{}"'
                    .format(description, str(caught_exception)))

    def drag_and_drop(self, source_element, destination_element,
                      source_element_description='', dest_element_description=''):
        """ Click and hold source_element and move it to destination_element.
        """
        source_webelement, source_webelement_des = self.initialize_webelement(source_element, source_element_description)
        dest_webelement, dest_webelement_des = self.initialize_webelement(destination_element, dest_element_description)
        try:
            action_chains = ActionChains(self.driver)
            action_chains.click_and_hold(source_webelement).move_to_element(dest_webelement).release(dest_webelement).perform()
        except Exception as e:
            raise CustomException("Failed to preform drag element : {} and drop to element {}. Got following exception"
                                  .format(source_webelement_des, dest_webelement_des, str(e)))

    # Input

    def send_keys(self, element, text_to_send='', el_description='', clear=True, click=True):
        """pasting keys into input or text field
        :param element : watch in description to this module
        :param el_description: watch in description to this module
        :param text_to_send: (str) text to set in a text field.
        :param clear (bool) if true - then clear filed before entering data.
        :param wait_to_be_enabled: (bool) if true - then wait for element to be enabled before entering keys.
        :param attempt (int) - not editable param.
        """
        web_element, description = self.initialize_webelement(element, el_description)
        if click:
            self.click(element, el_description)
        try:
            if clear:
                self.logger.info("Clearing following element '{}'".format(el_description))
                element.clear()

            if text_to_send:
                self.logger.info("Sending keys: '{}' on to following element '{}'".format(text_to_send, description))
                element.send_keys(text_to_send)

        except Exception as e:

            if not web_element.is_enabled():
                raise ElementIsDisabledException('Following element "{}" is disabled. '.format(el_description))

            raise ElementNotAvailableException('Failed to send keys to following element: "{}" due to caught exception: "{}"'
                                               .format(description, str(e)))

    def js_set_value_to_input(self, css_locator_of_element, keys):
        """"
        pass value to input_element (similar to send_keys) to
        input_element element using js executor.
        :param css_locator_of_element (str) locator of input_element (e.g. '.some_class input')
        :param keys (str) text to enter to input_element
        """
        try:
            self.logger.info("Settings following value: '{}' to element by css selector '{}'"
                             .format(keys, css_locator_of_element))
            self.driver.execute_script('document.querySelector("{}").value="{}"'
                                       .format(css_locator_of_element, keys))
        except Exception as e:
            raise JavascriptException("Failed to set value of input element, located by css selector: {}."
                                      "Got following exception: '{}'".format(css_locator_of_element, str(e)))

    # DROPDOWN

    def select_from_drop_down_by_text(self, list_of_options_from_dropdown, text_to_select, dropdown_to_expand=None,
                                      text_equals=False, el_description=None):
        """ Select value in dropdown if name contains specified name
        :param dropdown_to_expand: dropdown element to click. If None - expand actions will be not performed.
        :param el_description: description of dropdown element to click.
        :param list_of_options_from_dropdown: locator of child elements in dropdown to select
        :param text_to_select: (str) text to select from dropdown.
        :param text_equals: (bool) if true - that expected to find option with text, that equals text_to_select
        :return:
        """
        if dropdown_to_expand:
            dd_web_element, dd_description = self.initialize_webelement(dropdown_to_expand, el_description)
            self.logger.info("Clicking to open following dropdown '{}'".format(dd_description))
            self.click(dropdown_to_expand, el_description)
            time.sleep(3)

        if not self.is_element_displayed(list_of_options_from_dropdown):
            raise FlowFailedException("No options in dropdown list by locator '{}' found."
                                      .format(list_of_options_from_dropdown))

        option_elements_list, option_list_description = self.initialize_webelement(list_of_options_from_dropdown,
                                                                                   multiple=True)
        self.logger.info(
            "Selecting option with following text '{}' by locator '{}'".format(text_to_select, option_list_description))

        for option in option_elements_list:
            if text_to_select.lower() in option.text.lower():
                if not option.is_displayed():
                    continue
                if text_equals:
                    if text_to_select.lower() != option.text.lower():
                        continue
                self.logger.info('Found option with name: {}'.format(text_to_select))
                self.click(option, el_description=option_list_description, wait_to_be_enabled=False)
                return

        raise FlowFailedException(
            "No options in dropdown list by locator '{}' found that contains specified text : '{}'. {}"
            .format(option_list_description, text_to_select,
                    'Dropdown element: ' + el_description if el_description else ''))

    # CHECKBOX

    def is_checked(self, element, el_description=''):
        """return element is_checked status
        """
        web_element, description = self.initialize_webelement(element, el_description)
        try:
            self.logger.info("Getting is selected status of following checkbox '{}'".format(description))
            return element.is_selected()
        except Exception as e:
            raise ElementNotAvailableException('Failed to get is_selected status for element: "{}"'
                                               'Got following error: "{}"'.format(description, str(e)))

    def set_checkbox(self, element, el_description='', select=True):
        """set checkbox method
        select (bool)  if True - select checkbox (if it is not already selected);
                    if False - select checkbox (if it is not already selected);

        """
        web_element, description = self.initialize_webelement(element, el_description)

        if (select and not self.is_checked(element)) or (not select and self.is_checked(element)):
            self.logger.info("{} following checkbox: {}".format('selecting' if select else 'deselecting', description))
            self.click(element, el_description)

    # BROWSER

    def switch_to_window(self, index=None):
        """_"""
        self.logger.info("Switching to browser tab on index '{}'".format(str(index)))
        try:
            self.driver.switch_to_window(self.driver.window_handles[index])
        except (NoSuchWindowException, IndexError) as e:
            raise FlowFailedException(
                "Caught following exception when trying to switch to window by index \"{0}\"."
                "Total amount of windows: \"{1}\". Exception body: '{2}'"
                .format(str(index), len(self.driver.window_handles), str(e)))

    def browser_refresh(self):
        """Refreshes browser window. """
        self.logger.info("Refreshing browser...")
        return self.driver.refresh()

    # def accept_alert(self):
    #     """accept alert by clicking on ok btn in alert window"""
    #     self.logger.info("Accepting alert...")
    #     self.waits.wait_for_alert_is_present()
    #     alert = self.driver.switch_to.alert
    #     alert.accept()
    #
    # def alert_close(self):
    #     """close alert window (without any performed actions)"""
    #     self.logger.info("Closing alert...")
    #     self.waits.wait_for_alert_is_present()
    #     alert = self.driver.switch_to.alert
    #     alert.dismiss()
    #
    # def alert_send_keys_and_accept(self, keys):
    #     """enter keys into alert input field and accept alert"""
    #     self.logger.info("Sending keys: '{}' to alert input and accept".format(keys))
    #     self.waits.wait_for_alert_is_present()
    #     alert = self.driver.switch_to.alert
    #     alert.send_keys(keys)
    #     alert.accept()
