"""Interactions module. (Defining actions, that can be executed with elements
Common arguments, present in class methods of this module:

:param element :
                - or locator of element that is of tuple type :
                      e.g. ("CSS_SELECTOR", ".locator");
                      e.g. ("XPATH", "//*[@class ='class']"
                - or instance of class Element :
                      e.g. Element(self.session, ("CSS_SELECTOR", ".locator"))
                - or WebElement, that is already initialized.
:param description (str) - In case if element is of WebElement type - specify description of passed element.

"""
import time

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from base.configurations.element import Element
from base.configurations.waits import Waits
from base.configurations.exception import *

IMPLICITLY_TIMEOUT = 60


class InformationAboutElement:
    """ Mixin class that defines the commonly used interactions on a web page.
    """

    def __init__(self, session):
        self.driver = session.driver
        self.waits = Waits(session)
        self.logger = session.logger
        self.initialize_webelement = Element.initialize_webelement




class Getters(InformationAboutElement):
    """ Class describes all possible get operations from web-elements and
    their html/css properties.
    """
    def __init__(self, session):
        """
         :param session (obj) - instance of the session class
        """
        super(Getters, self).__init__(session)

    def get_text(self, element, description=None):
        """get inner text of element
        :param element : watch in description to this module
        :param description : watch in description to this module

        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Getting text from element '{}'".format(el_description))
        self.waits.wait_for_web_element_visible(element)
        try:
            return web_element.text.strip()
        except ElementNotInteractableException:
            if not web_element.is_enabled():
                raise ElementNotAvailableException("Can't get text from following element '{}' because it is not in the view or"
                                                   "not interactive".format(el_description))

    def get_attribute(self, element, description=None, attribute='value'):
        """get specified attribute from element
        :param element : watch in description to this module
        :param description: watch in description to this module
        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Getting attribute: '{}' from element '{}'".format(attribute, el_description))
        self.driver.implicitly_wait(IMPLICITLY_TIMEOUT)
        try:
            return web_element.get_attribute(attribute).lower()
        except NoSuchAttributeException:
            raise AttributeNotFoundException("Following element: '{}' has no attribute '{}'"
                                             .format(el_description, attribute))

    def get_element_location(self, element, description=None):
        """return dict , with {'y': '' , 'x': ''}  coordinates of an element.
        :param element : watch in description to this module
        :param description: watch in description to this module
         """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Getting location of element '{}'".format(el_description))
        location = web_element.location
        return location

    def get_css_value(self, element, css_property, description=None):
        """get value of specified css property of element
        :param css_property: (str) css property: e.g. 'display', 'height', 'width', etc.
        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Getting css value: '{}' from element '{}'".format(css_property, el_description))
        try:
            return web_element.value_of_css_property(css_property)
        except ElementNotInteractableException as exception:
            raise ElementNotAvailableException(
                "Can't get css property {} from following Element '{}'. Got following error {}"
                .format(css_property, el_description, str(exception)))


    def get_displayed_element_from_array(self, element, description=None, raise_exception=True):
        """Return first displayed element from array of WebElements.
        :param element : Locator of elements or already initialized list of WebElements.
        :param description: watch in description to this module
        :param raise_exception: (bool) if True raise FlowFailedException,
        if none of elements are displayed. Else - return None.

        :return Web Element that meets specified description and description of Web Element.
        """
        web_element, el_description = self.initialize_webelement(element, description, multiple=True)
        self.logger.info("Getting element from array of elements '{}', which is displayed".format(el_description))
        if web_element:
            for single_element in web_element:
                if single_element.is_displayed():
                    return single_element, el_description
        else:
            if raise_exception:
                raise FlowFailedException(
                    "No elements found by specified locator '{}'".format(el_description))

        if raise_exception:
            raise FlowFailedException(
                "No element in list of following elements ('{}') is displayed".format(el_description))
        return None, ''

    def get_element_from_array_by_text(self, element, text, description=None, text_equals=False, raise_exception=True):
        """ Return first element,  from array of WebElements,  that contains specified text.
         :param element : Locator of elements or already initialized list of WebElements.
        :param description: watch in description to this module
        :param text: (str) text to look for inside each of web_element.
        :param text_equals: (bool) if True - get web_element which text equals 'text' in param. Else
          get web_element which contains specified 'text'.
         :param raise_exception: (bool) if True raise FlowFailedException,
        if none of elements meets specified condition. Else - returns None.

        """
        web_element, el_description = self.initialize_webelement(element, description, multiple=True)
        self.logger.info("Getting element from array of elements '{}', which contains text '{}'"
                         .format(el_description, text))

        if web_element:
            for single_element in web_element:
                if text.lower() in single_element.text.lower():
                    if text_equals:
                        if text.lower() != single_element.text.lower():
                            continue
                    return single_element, el_description
        else:
            if raise_exception:
                raise FlowFailedException(
                    "No elements found by specified locator '{}'".format(el_description))

        if raise_exception:
            raise FlowFailedException(
                "No element in list of following elements ('{}') is displayed".format(el_description))
        return None, ''

    # def get_element_by_xpath_js(self, element):
    #     """
    #     Return DOM Node using
    #     XPATH for defining it on the page
    #     :param element: element xpath
    #     :return: DOM Node
    #     """
    #     return self.driver.execute_script("return document.evaluate(arguments[0],"
    #                                       " document, null, XPathResult.FIRST_ORDERED_NODE_TYPE,"
    #                                       " null).singleNodeValue", element)

class Scrolls(Getters):
    """Class that describes scroll actions on Web Pages."""

    def scroll_in_to_view(self, element, description=None):
        """ Scroll into the view of the element.
        :param element : watch in description to this module
        :param description : watch in description to this module.
        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Scrolling in to view of Element '{}'".format(el_description))

        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", web_element)
        except (NoSuchElementException, StaleElementReferenceException,
                ElementNotVisibleException, JavascriptException):
            raise CustomException('Failed to scroll to element "{}"'.format(el_description))

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

    def custom_scroll_to_element(self, element, description=None):
        """Custom scroll in the view (in the approximate view for web element)
        :param element : Locator of elements or already initialized list of WebElements.
        :param description: watch in description to this module
        """

        def get_visible_window_size(self):
            """returns visible window size (half of the total page height)"""
            return int(self.driver.execute_script('return window.outerHeight') / 2)

        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Make custom scroll to element '{}'".format(el_description))

        x_attr, y_attr = web_element.location.values()
        self.driver.execute_script("window.scrollTo(%s, %s)" % (x_attr, y_attr - get_visible_window_size(self)))

    # def custom_scroll_to_element_version_2(self, webelement):
    #     """
    #     Scroll to specified web element, when you stack with navigation bar
    #     :param webelement: selenium webelement
    #     """
    #
    #     def get_navbar_size():
    #         ind = []
    #         for navbar in Element(self.driver, ('CSS_SELECTOR', 'div.navbar'))(multiple=True):
    #             ord_attr = navbar.rect['height']
    #             ind.append(ord_attr)
    #         return ind
    #
    #     def navbar_size():
    #         navbar_size = 0
    #         for size in get_navbar_size():
    #             navbar_size += size
    #         return navbar_size
    #
    #     tuple, element = self.wait.wrapped_element(webelement)
    #     abs_attr, ord_attr = element.location.values()
    #     self.driver.execute_script("window.scrollTo(%s, %s)" % (abs_attr, ord_attr - navbar_size()))

class ClickHoverDrugAndDrop(Scrolls):
    """ Mixin class that defines the commonly used interactions on a web page.
    """

    def click(self, element, description=None, wait_to_be_enabled=True, attempt=0):
        """perform click on element
       :param element : watch in description to this module
       :param description: watch in description to this module
       :param wait_to_be_enabled: (bool) if true - then wait for element to be enabled before entering keys.
        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Clicking on following element '{}'".format(el_description))


        if wait_to_be_enabled:
            self.waits.wait_for_element_to_be_enabled(element, description)
        try:
            self.logger.info("Clicking on following element '{}'".format(el_description))
            web_element.click()

        except StaleElementReferenceException:
            if attempt == 0:
                self.logger.info('Caught StaleElementReferenceException exception on following element "{}". '
                                 'Repeating in 5 seconds.'.format(el_description))
                time.sleep(5)
                self.click(element, description, wait_to_be_enabled, attempt=1)
            else:
                raise StaleElementReferenceException('Following element "{}" is stale. '.format(el_description))

        except ElementNotInteractableException:
            if not web_element.is_enabled():
                raise ElementIsDisabledException('Following element "{}" is disabled. '.format(el_description))

            if attempt == 0:
                self.logger.info("Element: '{}' is not interactive. Retrying with scrolling.".format(el_description))
                self.custom_scroll_to_element(element)
                self.click(element, description, wait_to_be_enabled, attempt=1)
            else:
                raise ElementNotAvailableException('Following element "{}" is not in the view or can`t be interacted.'
                                                   .format(el_description))


    def click_by_coordinates(self, element, description=None, xoffset=0, yoffset=0):
        """ Performs a click on coordinates, relative to element location.
        (top left corner of element)
        Args:
            element : watch in description to this module
            description: watch in description to this module
            xoffset (int): offset from center of element coordinates by x axis to click.
            yoffset (int): offset from center of element coordinates by y axis to click.
        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Clicking on following element '{}' with x_offset: '{}', y_offset: '{}'"
                         .format(el_description, xoffset, yoffset))

        action_chains = ActionChains(self.driver)
        try:
            action_chains.move_to_element(element).move_by_offset(xoffset, yoffset).click().perform()

        except Exception as caught_exception:
            raise CustomException(
                    'Failed to click on element: "{}", with offset by x coordinates : {} and y coordinates : {}.'
                    'Caught following exception: "{}"'
                    .format(el_description, str(xoffset), str(yoffset), str(caught_exception)))

    def hover(self, element, description=None, xoffset=0, yoffset=0):
        """ Performs a mouseover/hover on element
        Moves mouse to the middle of the element

        Args:
            webelement (object): selenium webelement to double click on
            xoffset (int): offset from upper left to click on element
            yoffset (int): offset from upper left to click on element
        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Hovering on following element '{}'".format(el_description))
        action_chains = ActionChains(self.driver)
        try:
            if xoffset > 0 or yoffset > 0:
                action_chains.move_to_element_with_offset(element, xoffset, yoffset).perform()
            else:
                action_chains.move_to_element(web_element).perform()

        except Exception as caught_exception:
            raise CustomException(
                    'Failed to hover on element: "{}", with offset by x coordinates : {} and y coordinates : {}.'
                    'Caught following exception: "{}"'
                    .format(el_description, str(xoffset), str(yoffset), str(caught_exception)))

    def drag_and_drop(self, source_element, source_el_description, dest_element, dest_element_description):
        """ Click and hold element to drag and move it to element to drop.
        """
        web_element_source, source_description = self.initialize_webelement(source_element, source_el_description)
        web_element_dest, dest_description = self.initialize_webelement(dest_element, dest_element_description)
        self.logger.info("Drug element: '{}'. Drop to element '{}'".format(source_description, dest_description))

        action_chains = ActionChains(self.driver)
        try:
            action_chains.click_and_hold(web_element_source)\
                .move_to_element(web_element_dest).release(web_element_dest).perform()
        except Exception as caught_exception:
            raise CustomException('Caught following exception when trying to drag element: "{}"'
                                  'and drop to element: "{}". Exception body: "{}"'
                                  .format(source_description, dest_description, str(caught_exception)))

    # def double_click(self, element, description=None):
    #     """ Double clicks on the webelement supplied
    #     """
    #     web_element, el_description = self.initialize_webelement(element, description)
    #     self.logger.info("Making double click on element '{}'".format(el_description))
    #     action_chains = ActionChains(self.driver)
    #     try:
    #         action_chains.double_click(web_element).perform()
    #     except Exception as caught_exception:
    #         raise CustomException('Caught following exception when trying to perform double click on element : "{}"'
    #                               'Exception body: "{}"'.format(el_description, str(caught_exception)))


    # def right_click(self, element, description=None):
    #     """Right mouse click on some element"""
    #     web_element, el_description = self.initialize_webelement(element, description)
    #     self.logger.info("making right click on following element '{}'".format(el_description))
    #     action_chains = ActionChains(self.driver)
    #     try:
    #         action_chains.context_click(web_element).perform()
    #     except Exception as caught_exception:
    #         raise CustomException('Caught following exception when trying to perform double click on element : "{}"'
    #                               'Exception body: "{}"'.format(el_description, str(caught_exception)))


class Input(ClickHoverDrugAndDrop):
    """Class that defines interactions with 'input', 'text box', iframe
    elements."""

    def send_keys(self, element, keys, description=None, clear=True, wait_to_be_enabled=True, attempt=0):
        """pasting keys into input or text field
        :param element : watch in description to this module
        :param description: watch in description to this module
        :param keys: (str) text to set in a text field.
        :param clear (bool) if true - then clear filed before entering data.
        :param wait_to_be_enabled: (bool) if true - then wait for element to be enabled before entering keys.
        :param attempt (int) - not editable param.
        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Sending keys: '{}' on to following element '{}'".format(keys, el_description))
        if wait_to_be_enabled:
            self.waits.wait_for_element_to_be_enabled(element, description)

        try:
            if clear:
                self.logger.info("Clearing following element '{}'".format(el_description))
                element.clear()
            self.logger.info("Sending keys '{}' to following element '{}'".format(keys, el_description))
            element.send_keys(keys)
        except StaleElementReferenceException:
            if attempt == 0:
                self.logger.info('Caught StaleElementReferenceException exception on following element "{}". '
                                 'Repeating in 5 seconds.'.format(el_description))
                time.sleep(5)
                self.send_keys(element, keys, description, clear, wait_to_be_enabled, attempt=1)
            else:
                raise StaleElementReferenceException('Following element "{}" is stale. '.format(el_description))

        except ElementNotInteractableException:
            if not web_element.is_enabled():
                raise ElementIsDisabledException('Following element "{}" is disabled. '.format(el_description))

            if attempt == 0:
                self.logger.info("Element: '{}' is not interactive. Retrying with scrolling.".format(el_description))
                self.custom_scroll_to_element(element)
                self.send_keys(element, keys, description, clear, wait_to_be_enabled, attempt=1)
            else:
                raise ElementNotAvailableException('Following element "{}" is not in the view or can`t be interacted.'
                                                   .format(el_description))

    def set_file_path(self, element, path_to_file, description=None, attempt=0):
        """Entering path to a file into file input element.
       :param element : watch in description to this module
        :param description: watch in description to this module
        :param path_to_file : (str) path to file.
        """
        web_element, el_description = self.initialize_webelement(element, description)

        self.logger.info("Sending path '{}' to following element '{}'".format(path_to_file, el_description))
        try:
            element.send_keys(path_to_file)
        except StaleElementReferenceException:
            if attempt == 0:
                self.logger.info('Caught StaleElementReferenceException exception on following element "{}". '
                                 'Repeating in 5 seconds.'.format(el_description))
                time.sleep(5)
                self.set_file_path(element, path_to_file, description, attempt=1)
            else:
                raise StaleElementReferenceException('Following element "{}" is stale. '.format(el_description))

        except ElementNotInteractableException:
            if attempt == 0:
                self.logger.info("Element: '{}' is not interactive. Retrying with scrolling.".format(el_description))
                self.custom_scroll_to_element(element)
                self.set_file_path(element, path_to_file, description, attempt=1)
            else:
                raise ElementNotAvailableException('Following element "{}" is not in the view or can`t be interacted.'
                                                   .format(el_description))

    def js_set_value_to_input(self, css_locator_of_element, keys):
        """"
        pass value to input_element (similar to send_keys) to
        input_element element using js executor.
        :param css_locator_of_element (str) locator of input_element (e.g. '.some_class input')
        :param keys (str) text to enter to input_element
        """
        try:
            self.logger.info("Settings following value: '{}' to element by locator '{}'"
                             .format(keys, css_locator_of_element))
            self.driver.execute_script('document.querySelector("{}").value="{}"'
                                       .format(css_locator_of_element, keys))
        except JavascriptException:
            raise JavascriptException("Failed to send value to input by locator: {}"
                                      .format(css_locator_of_element))


    def clear_input(self, element, description=None, attempt=0):
        """clear text filed or input"""
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Clearing up following element '{}'".format(el_description))
        try:
            self.logger.info('Clearing up following element "{}". '.format(el_description))
            web_element.clear()
        except StaleElementReferenceException:
            if attempt == 0:
                self.logger.info('Caught StaleElementReferenceException exception on following element "{}". '
                                 'Repeating in 5 seconds.'.format(el_description))
                time.sleep(5)
                self.clear_input(element, description, attempt=1)
            else:
                raise StaleElementReferenceException('Following element "{}" is stale. '.format(el_description))

        except ElementNotInteractableException:
            if not web_element.is_enabled():
                raise ElementIsDisabledException('Following element "{}" is disabled. '.format(el_description))

            if attempt == 0:
                self.logger.info("Element: '{}' is not interactive. Retrying with scrolling.".format(el_description))
                self.custom_scroll_to_element(element)
                self.clear_input(element, description, attempt=1)
            else:
                raise ElementNotAvailableException('Following element "{}" is not in the view or can`t be interacted.'
                                                   .format(el_description))

    # def set_value_in_iframe(self, iframe_element, text):
    #     """
    #     Switch to specified 'iframe' element.
    #     Clear and send text within iframe_element. Switch back
    #     to main html, after finishing.
    #     :param iframe_element: (tuple) locator of specified iframe element
    #     :param text: (str) text to send to element.
    #     """
    #     self.driver.switch_to.frame(iframe_element())
    #     input_elem = self.driver.find_element_by_xpath("/html/body")
    #     self.send_keys(input_elem, text)
    #     input_elem.send_keys(Keys.CONTROL, 'a') # need to fix
    #     self.driver.switch_to.default_content()


class Dropdown(Input):
    """Class that defines interactions with 'drop down' element."""

    def select_from_drop_down_by_text(self, list_of_options_from_dropdown, text_to_select, dropdown_to_expand=None,
                                      text_equals=False, description=None):
        """ Select value in dropdown if name contains specified name
        :param dropdown_to_expand: dropdown element to click. If None - expand actions will be not performed.
        :param description: description of element to click.
        :param list_of_options_from_dropdown: locator of child elements in dropdown to select
        :param text_to_select: (str) text to select from dropdown.
        :param text_equals: (bool) if true - that expected to find option with text, that equals text_to_select
        :return:
        """
        if dropdown_to_expand:
            dropdown_element, dropdown_description = self.initialize_webelement(dropdown_to_expand, description)
            self.logger.info("Clicking to open following dropdown '{}'".format(dropdown_description))
            self.click(dropdown_to_expand, description=description)
            try:
                self.waits.wait_for_number_of_elements_present(list_of_options_from_dropdown)
            except (ElementNotFoundExcepiton, FlowFailedException):
                raise FlowFailedException("Following dropdown : '{}' has no options to select (is empty)"
                                          .format(dropdown_description))

        option_elements_list, option_list_description = self.initialize_webelement(list_of_options_from_dropdown, multiple=True)
        self.logger.info("Selecting option with following text '{}' by locator '{}'".format(text_to_select, option_list_description))

        for option in option_elements_list:
            if text_to_select.lower() in option.text.lower():
                if not option.is_displayed():
                    continue
                if text_equals:
                    if text_to_select.lower() != option.text.lower():
                        continue
                self.logger.info('Found option with name: {}'.format(text_to_select))
                self.click(option, description='option_list_description', wait_to_be_enabled=False)
                return

        raise FlowFailedException("No elements in list of dropdown options ('{}') found that contains specified text : '{}'"
                                  .format(option_list_description, text_to_select))

    def select_option_from_dropdown(self, dropdown_element, option_name, description=None):
        """
        Method to choose option from dropdown of type 'select'
        :param dropdown_element: (webelement, tuple): dropdown element which has 'select' tag name
        :param option_name: (str) name of option
        """
        web_element, el_description = self.initialize_webelement(dropdown_element, description)
        self.logger.info("Selecting option with following text: '{}' in following dropdown: {}'"
                         .format(option_name, el_description))


        self.waits.wait_for_web_element_visible(dropdown_element)
        try:
            Select(web_element).select_by_visible_text(option_name)
        except NoSuchElementException:
            raise FlowFailedException('No options found in dropdown {} that contains text'.format(dropdown_element, option_name))


class Checkbox(Dropdown):
    """Class that defines interactions with 'checkbox' element."""

    def set_checkbox(self, element, description=None, select=True, attempt=0):
        """select/deselect specified checkbox.
        :param element : watch in description to this module
        :param description: watch in description to this module
        :param select: (bool) if True - perform select checkbox. Else - deselect.
        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("{} following checkbox : '{}'".format('selecting' if select else 'deselecting', el_description))

        if select and self.is_element_selected(element, description):
            return

        if not select and not self.is_element_selected(element, description):
            return

        try:
            self.click(element, description)

        except StaleElementReferenceException:
            if attempt == 0:
                self.logger.info('Caught StaleElementReferenceException exception on following element "{}". '
                                 'Repeating in 5 seconds.'.format(el_description))
                time.sleep(5)
                self.set_checkbox(element, description, select, attempt=1)
            else:
                raise StaleElementReferenceException('Following element "{}" is stale. '.format(el_description))

        except ElementNotInteractableException:
            if not web_element.is_enabled():
                raise ElementIsDisabledException('Following element "{}" is disabled. '.format(el_description))

            if attempt == 0:
                self.logger.info("Element: '{}' is not interactive. Retrying with scrolling.".format(el_description))
                self.custom_scroll_to_element(element)
                self.set_checkbox(element, description, select, attempt=1)
            else:
                raise ElementNotAvailableException('Following element "{}" is not in the view or can`t be interacted.'
                                                   .format(el_description))

    def set_checkbox_in_table_by_text(self, text, parent_xpath_locator='', is_radio_button=False,
                                           select=True):
        """Select/deselect checkbox in table row, that contains specified text.
        :param text (str) text to search within table row
        :param parent_xpath_locator (str) xpath locator of the parent scope (such as modal body or specified block)
        in case if several tables are present in DOM structure. e.g. "//*[@class ='.modal-body']"
        :param is_radio_button (bool) specify true or false for clarifying selector.
        :param select : (bool) select/deselect
        """

        def locators(text):
            """
            :param text:
            :return:
            """
            return (
                ("XPATH", parent_xpath_locator + " //*[./text()='{}']//ancestor::tr".format(text)),  # any element, where text == inner text.
                ("XPATH", parent_xpath_locator + " //*[contains(text(), '{}')]//ancestor::tr".format(text)),  # any element, where text in inner text.
                ("XPATH", parent_xpath_locator + " //*[. = '']/ancestor::tr".format(text))  # any attribute, where text in inner text.
            )

        def get_locator(text):
            """
            :param text:
            :return:
            """
            for i in range(len(locators(text)) - 1):
                test_locator = Element(self.session, locators(text)[i])(multiple=True, implicitly_timeout=3)
                if test_locator:
                    return locators(text)[i]
            raise FlowFailedException('No rows found in table, that contains text : "{}".'.format(text))

        self.logger.info("{} checkbox in table row with text: '{}'".format('selecting' if select else 'deselecting', text))
        row_locator = get_locator(text)
        if is_radio_button:
            row_locator += " //input[@type='checkbox']"
        else:
            row_locator += " //input[@type='radio']"
        if Element(self.session, row_locator)(multiple=True, implicitly_timeout=3):
            self.set_checkbox(row_locator, select=select)
        else:
            raise ElementNotFoundExcepiton('Quantity of checkboxes found within locator : "{}"'
                                           ' is 0.'.format(row_locator))

class EventHandlers(Checkbox):
    """ Class descries common events, to deal with on UI.
    """

    def modals_handling(self, modal_locator, button, timeout=5):
        """ Wait, if element present and element visible, then perform click on
        some child element. Else - no action will be performed.
        :param modal_locator: (tuple) locator of modal window or other pop-up element
        :param button: (tuple) locator of element to click if first present.
        :param timeout (int) time to wait for modal present.
        """
        self.logger.info("Start modals handling")
        if self.is_elements_present(modal_locator, timeout=timeout):
            if self.waits.wait_for_web_element_visible(modal_locator, timeout=timeout, raise_exception=False):
                self.click(button)

    def handle_events_after_save(self, error_modal_window, toaster_locator=None):
        """
        :param error_modal_window: (tuple) expected locator of error modal window to be
        if error is present
        :param toaster_locator: (tuple) specified locator for success toaster.
        :return:
        """
        self.logger.info("Start checking for success notification present")
        try:
            if toaster_locator:
                self.waits.wait_for_web_element_visible(toaster_locator)
            else:
                toaster = Element(self.session, ("CSS_SELECTOR", ".xwt-success-message"))
                self.waits.wait_for_web_element_visible(toaster)
                # assert "success" in toaster().text.lower()
        except (ElementNotFoundExcepiton, FlowFailedException):
            if self.is_elements_present(error_modal_window):
                raise FlowFailedException("Save failed. Error modal is present on. Text inside error modal: '{}'."
                                          .format(error_modal_window().text))
            raise FlowFailedException(
                "Success toaster was not found or is invisible. Operation failed.")

    def handle_event_with_modal_after_action(self, error_modal_window, action_message="", timeout=5,
                                             raise_exception=True):
        """
        Handling error / warning popups after
        some action (e.g click on button / send text to input)
        :param error_modal_window: expected error modal in case if something
        went wrong
        :param action_message: optional argument. Describes specified action
        message (e.g "clicking on Add button")
        :param raise_exception(bool) option to raise exception or not if error modal present.
        :param timeout(int) time to wait error modal to be present.

        :return True  - if error message is present; False - is not present.
        """
        self.logger.info("Start checking if error modal present after action: '{}'".format(action_message))
        if self.is_elements_present(error_modal_window, timeout=timeout):
            if raise_exception:
                raise FlowFailedException(
                        "Error modal appeared after following actions: '{}'. Text inside error modal: '{}'"
                        .format(action_message, error_modal_window().text))
            else:
                self.logger.info("Found error modal after performing following actions: '%s'." % action_message)
                return True
        else:
            self.logger.info("No errors found after %s action.", action_message)
            return False

    def handle_loader(self, loader, time_appear=10, time_disappear=10):
        """
        Wait for loader to disappear , if it is present
        :param loader: (tuple) locator of loader
        :param time_appear: (int) time to wait for loader present
        :param time_disappear: (int) time to wait for loader disappear
        :return:
        """
        self.logger.info("Start loader handling")
        if self.is_elements_present(loader, timeout=time_appear):
            self.waits.wait_for_web_element_not_visible(loader, timeout=time_disappear)


class BrowserNative(EventHandlers):
    """class that defines native selenium interactions with browser"""

    def switch_to_window(self, index=None):
        """_"""
        self.logger.info("Switching to browser tab with on index '{}'".format(str(index)))
        if index is None:
            for tab in self.driver.window_handles:
                self.driver.switch_to_window(tab)
        else:
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

    def accept_alert(self):
        """accept alert by clicking on ok btn in alert window"""
        self.logger.info("Accepting alert...")
        self.waits.wait_for_alert_is_present()
        alert = self.driver.switch_to.alert
        alert.accept()

    def alert_close(self):
        """close alert window (without any performed actions)"""
        self.logger.info("Closing alert...")
        self.waits.wait_for_alert_is_present()
        alert = self.driver.switch_to.alert
        alert.dismiss()

    def alert_send_keys_and_accept(self, keys):
        """enter keys into alert input field and accept alert"""
        self.logger.info("Sending keys: '{}' to alert input and accept".format(keys))
        self.waits.wait_for_alert_is_present()
        alert = self.driver.switch_to.alert
        alert.send_keys(keys)
        alert.accept()


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
            self.logger.info("Start checking if element present {}".format(el_description))
            self.initialize_webelement(element,  timeout=timeout)
            self.logger.info('Found following element: {}'.format(element))
            return True
        except ElementNotFoundExcepiton:
            self.logger.info('Element by locator "{}" not found. Waited for  "{}"'.format(element, timeout))
            return False


    def is_element_displayed(self, element, description=None, raise_excepton=False):
        """return element is_displayed status by selenium operator.
        :param element : watch in description to this module
        :param description: watch in description to this module

        :raise ElementNotFoundExcepiton if element not present or not displayed and raise_excepton = True
        """
        try:
            web_element, description = self.initialize_webelement(element, description)
            self.logger.info("Start checking if element '{}' is displayed".format(description))
            if web_element.is_displayed():
                return True
            else:
                if raise_excepton:
                    raise ElementNotAvailableException("Following element : '{}' is not displayed.".format(description))
                return False

        except ElementNotFoundExcepiton:
            if raise_excepton:
                raise ElementNotFoundExcepiton("Following element : '{}' is not present in DOM.".format(description))
            return False

    def is_element_selected(self, element, description=None):
        """return element is_checked status by selenium operator.
        :param element : watch in description to this module
        :param description: watch in description to this module
        """
        web_element, el_description = self.initialize_webelement(element, description)
        self.logger.info("Start checking if element '{}' is selected".format(el_description))
        try:
            return web_element.is_selected()
        except Exception as exception:
            raise CustomException("Failed to get selected/unselected status of following element : '{}' "
                                  "due to following exception: '{}'".format(el_description, str(exception)))

    def is_element_selected_js(self, css_selector_of_element):
        """return element is_checked status by JS operator"""
        try:
            self.logger.info("Start checking if element '{}' is selected".format(css_selector_of_element))
            return self.driver.execute_script("return document.querySelector("
                                              "argument[0]).checked", css_selector_of_element)
        except JavascriptException:
            raise JavascriptException("Failed to check if element by locator '{}' is selected"
                                      .format(css_selector_of_element))


