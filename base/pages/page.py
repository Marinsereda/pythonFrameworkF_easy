"""Module describes Page."""
from random import randint
from selenium.common.exceptions import WebDriverException
from base.base import Base
from base.configurations.element import Element
from base.configurations.interactions import Interactions
from base.configurations.exception import *


class Page(Base):
    """Describes Base Page Element. And common methods for all page objects"""
    def __init__(self, page_config, run_validations=True):
        super().__init__(page_config)
        if self.launch:
            self.login(self.credentials)
            # self.license_popup_handler()
            self.navigate_to_page()
        else:
            self.navigate_to_page()
        self.avoid_optional_disasters()
        self.navigate_if_tabbed()
        if run_validations:
            self.run_validations()
        self.close_session_info_toaster()


    def run_custom_validation(self, validation, timeout=60):
        """
        :param validation:  key of dict
        :return:
        """
        if hasattr(self.config, 'CUSTOM_VALIDATIONS'):
            items_to_validate = [
                item_to_validate for item_to_validate in
                self.config.CUSTOM_VALIDATIONS if validation in item_to_validate
            ]
            for item in items_to_validate:
                self.prepare_validations_arr(item, timeout)

    def avoid_optional_disasters(self):
        """
        Check if "OPTIONAL_DISASTERS" attribute was defined in page config
        start manipulations with optional disasters to avoid them
        """
        if hasattr(self.config, "OPTIONAL_DISASTERS"):
            LOGGER.info("OPTIONAL_DISASTERS attribute was defined in the config. "
                        "Starting optional disasters avoidance process.")
            for opt_disaster in self.config.OPTIONAL_DISASTERS:
                self.avoid_optional_disaster(opt_disaster)
        else:
            LOGGER.info("OPTIONAL_DISASTERS attribute was not defined in the page config. "
                        "Skipping optional disasters avoidance process.")

    def avoid_optional_disaster(self, disaster):
        """_"""
        disaster_element = disaster.get("element")
        disaster_wait_action = disaster.get("action")
        disaster_avoid_action = disaster.get("avoid_action")
        LOGGER.info("Work around {} disaster".format(str(disaster_element)))
        self.call_disaster_wait_action(disaster_wait_action, disaster_element)
        self.call_disaster_avoid_action(disaster_avoid_action, disaster_element)

    @property
    def disaster_wait_dict(self):
        """_"""
        return {
            "wait_for_web_element_visible": self.waits.wait_for_web_element_visible
        }

    @property
    def disaster_avoid_dict(self):
        """_"""
        return {
            "click": self.action.click
        }

    def get_disaster_wait_action(self, wait_action):
        """_"""
        return self.disaster_wait_dict[wait_action]

    def get_attr_element(self, element, attribute):
        """
        :param element (tuple): locator for handling
        :param attribute (str): element's attribute
        :return (str): attribute of element
        """
        return self.action.get_attribute(element, attribute)

    def get_css_value(self, element, style):
        """
        :param element (tuple): webelement
        :param style (str): name of style
        :return (str): element's css_property value
        """
        return self.action.value_of_css_property(element, style)

    @staticmethod
    def generate_random_ip():
        """generate random IP"""
        random_ip = ''
        for _ in range(0, 4):
            random_ip += '.' + str(randint(0, 255))
        return random_ip[1:]

    def call_disaster_wait_action(self, wait_action, disaster_element):
        """_"""
        return self.get_disaster_wait_action(wait_action)(disaster_element)

    def get_disaster_avoid_action(self, avoid_action):
        """_"""
        return self.disaster_avoid_dict[avoid_action]

    def call_disaster_avoid_action(self, avoid_action, avoid_element):
        """_"""
        return self.get_disaster_avoid_action(avoid_action)(avoid_element)

    def verify_text_in_modal_window(self, modal_window_locator, text):
        """
        Check specified text is in the text of modal window
         :param (str) text: text to check

        """
        if  text not in self.action.get_text(modal_window_locator):
            raise FlowFailedException("Expected text : '{0}' is not contained in text of "
                                      "modal window found by locator: '{1}'"
                                      .format(text, modal_window_locator))

    def verify_if_element_displayed(self, elem):
        """wait for element to be displayed
        Raise ElementNotFoundException if element is not visible."""
        self.waits.wait_for_web_element_visible(elem)

    def verify_deploy_process_popup_occured(self):
        """Verify Deploy popup in SecurityGroups and SecurityGroupACLs"""
        LOGGER.info("Started verification of the 'Verify Deploy' popup in SecurityGroups")
        self.action.handle_info_popup()
        self.action.close_info_popup()

    def is_element_present(self, element, timeout):
        """
        :param element (tuple): element
         :param timeout (str): time to wait for element
        :return (bool): Boolean condition of presence element
        """
        return self.action.is_custom_elements_present(element, timeout)

    def set_specifed_checkbox(self, checkbox_locator, select=True):
        """set checkbox by specified locator
        :param checkbox_locator : (tupple) checkbox locator
         :param select : (tupple) if true - activate checkbox.
         Else - uncheck checkbox.
        """
        self.action.set_checkbox(checkbox_locator, select)

    def send_text_to_input(self, element, text, clear=True):
        """send text to specified input"""
        self.action.send_keys(element, text, clear=clear)

    def click_specifed_radio_button(self, radio_button_locator):
        """click radio button by specified locator"""
        self.action.click(radio_button_locator)
        # if not Element(self.session.driver, radio_button_locator)().is_selected():
        if not self.action.is_checked(Element(self.session.driver, radio_button_locator)()):
            raise FlowFailedException("Radio button by locator  '{}' was not"
                                      " selected after clicking on it"
                                      .format(radio_button_locator))
    def click_on_cancel(self):
        """click on cancel button"""
        self.action.click(self.cancel_btn)

    def click_on_save(self):
        """
        Clicking on save btn. Before clicking on save checks if all field are valid.
        :param (tuple) save_btn: locator of button 'save'.
        """
        form_validation_error = ("CSS_SELECTOR", ".has-error")
        if self.action.check_is_element_present_in_dom(
                form_validation_error, timeout=5):
            raise FlowFailedException('Invalid data are typed in the form fields.')
        self.action.scroll_in_to_view(self.save_btn())
        self.action.click(self.save_btn)
        self.check_validation_error()

    def check_validation_error(self, raise_exception=True):
        """Check if validation error present"""
        validation_error_locator = ("CSS_SELECTOR", ".has-error")
        validation_error = Element(self.session.driver, validation_error_locator)
        if self.action.check_is_element_present_in_dom(validation_error_locator, timeout=2):
            if raise_exception:
                raise FlowFailedException('Following validation error is present on page : "{}"'
                                          .format(validation_error().text))
            else:
                LOGGER.info('Validation error found on page : "{}". Check correctness of filled data.'
                            .format(validation_error().text))
                return True
        return False

    def check_element_is_enabled(self, element, element_description='', raise_exception=True):
        """Check if passed element is enabled.
        :param element (obj) WebElement
        :param raise_exception (bool) if True - raise exception if element is disabled.
        """

        if element.is_enabled():
            return True
        else:
            if raise_exception:
                raise FlowFailedException('Following element: "{}" is disabled.'
                                          .format(element_description))
            else:
                LOGGER.info('Following element: "{}" is disabled.'.format(element_description))
                return False

    def click_to(self, element, wait_to_be_clickable=True):
        """
        To click element
        :param element (tuple): element
        """
        self.action.click(element, wait_to_be_clickable=wait_to_be_clickable)

    def check_if_dirty_modal_and_skip(self):
        """
        Check if dirty page modal window is present
        and confirm leave action
        """
        if self.is_element_present(self.backbone_warning_modal, timeout=5):
            LOGGER.info("Found Backbone Dirty page modal. Click confirm.")
            self.action.click(self.dirty_page_modal_ok_btn)
            self.waits.wait_for_web_element_not_visible(self.backbone_warning_modal)
        elif self.is_element_present(self.dojo_warning_modal, timeout=5):
            LOGGER.info("Found Dojo Dirty page modal. Click confirm.")
            self.action.click(self.dojo_dirty_page_modal_ok_btn)
            self.waits.wait_for_web_element_not_visible(self.dojo_warning_modal)
        else:
            LOGGER.info("Did not find any Dirty Page Modal windows.")

    def set_value_for_token_panel(self, options, repeater=True):
        """
        To select option from token panel
        :param column_arrow (tuple): locator of column arrow to expand token field
        :param options (dict):
                example of dicts (key - (str) to get value,
                value - (str) or (dict) - options text
                                'identity_groups': {'Any': None,
                                            'User Identity Group': 'Employee',
                                            'Endpoint Identity Group': 'Blacklist'},

                                'os': { 'Windows All': {'Windows 7 (All)': '7 Enterprise'}},
        """
        def is_last_option(option):
            return '_flag' in option

        def add_flag(option):
            return option + '_flag'

        def get_last_repeater_element(element):
            return element(multiple=True)[-1]

        def get_options():
            list_of_options = []

            for key, value in options.items():
                if value:
                    list_of_options.append(key)
                    if isinstance(value, dict):
                        for k, val in value.items():
                            # if val:
                            list_of_options.append(k)
                            list_of_options.append(add_flag(val))
                            # else:
                            #     list_of_options.append(add_flag(k))
                    else:
                        list_of_options.append(add_flag(value))
                else:
                    list_of_options.append(add_flag(key))
            return list_of_options

        def get_element(self):
            self.waits.wait_for_web_element_visible(self.popup_repeater_dropdown_container_list)
            for element in self.popup_repeater_dropdown_container_list(multiple=True):
                for text in self.options:
                    if text.split('_')[0] in element.text:
                        self.options.remove(text)
                        return element, text
            return None

        def set_option(self):
            self.action.is_custom_elements_present(element="#list", timeout=6)
            element, text = get_element(self)
            if is_last_option(text):
                self.action.click(element)
                # element.click()
            else:
                try:
                    self.action.click(element.find_element_by_css_selector("[id ='osItemNavNode']"))
                    # element.find_element_by_css_selector("[id ='osItemNavNode']").click()
                except WebDriverException as ex:
                    if 'unknown error' in str(ex):
                        self.action.click(element)
                        # element.click()
                    else: raise SeleniumException("Can't click on element %s" % element)
                set_option(self)

        self.options = get_options()
        option = 0
        for _ in range(len(options)):
            if repeater:
                self.waits.wait_for_web_element_visible(self.popup_repeater_dropdown)
                self.action.click(
                    get_last_repeater_element(self.popup_repeater_dropdown))
                # get_last_repeater_element(self.popup_repeater_dropdown).click()
            set_option(self)
            if (len(options)-option) > 1:
                option += 1
                self.action.click(get_last_repeater_element(
                    self.popup_repeater_plus_btn))
                # get_last_repeater_element(self.popup_repeater_plus_btn).click()
                # self.action.scroll_in_to_view(get_last_repeater_element(
                #     self.popup_repeater_dropdown))
        self.action.click(self.default)

    def reset_token_pannel_to_default(self, wait_time):
        """click on back arrow in token panel until it gets disabled."""
        while not self.action.is_custom_elements_present(self.naviagte_back_token_panel_btn_disabled, timeout=2):
            self.action.click(self.naviagte_back_token_panel_btn)
            self.wait_token_panel_loaded(wait_time, 30)

    def set_value_for_token_panel_2(self, options, wait_panel_closed=True, reset_pannel=False,
                                    wait_time=8):
        """ Select value from object selector panel (without repeater)
        Select value from object selector dropdown. Method perform clicking on
        chain of elements, that contains specified text.
        Method doesn't perform clicking on expand (open panel) button.
        :param options: (dict) :
        example of config files to perform select from 'object selector panel' element:
        1) Simple select. Use a pair of key - value.  Key - could be or name of item in list
           or folder name to be clicked.  Value - should be final name of item to be clicked.
           config  = {'Radius': 'Callback'}
        2) Drill down select. Use nested dictionaries.
        Values in dict could be or name of items in list
        or folders. Last element in dict chain should be final item to click.
                config = {'os': {
                                'Windows': '7',
                                },
                          }
        :param wait_panel_closed (bool) if true - wait for token panel to be closed after
        option is selected.
        :param wait_time (int) second to wait for loader (spinner) to appear on each step
        of selection.
        """
        self.wait_token_panel_loaded(wait_time, 30)
        if reset_pannel:
            self.reset_token_pannel_to_default(wait_time)
        self.options = self.get_options(options)
        for i, option in enumerate(self.options):
            try:
                self.set_option(option, wait_panel_closed, wait_time)
            except FlowFailedException:
                self.waits.wait_for_web_element_not_visible(self.object_selector_load_indicator)
                self.set_option(option, wait_panel_closed, wait_time)


    def wait_token_panel_loaded(self, time_loader_appear, time_loader_disappear):
        """wait for loader appeared/disappeared and token panel is in ready state"""
        self.waits.wait_for_web_element_visible(self.popup_repeater_dropdown_container_list)
        self.action.handle_loader(self.object_selector_load_indicator,
                                  time_loader_appear,
                                  time_loader_disappear)

    def set_value_for_tokenpanel_dropdown_v3(self, dropdown, list):
        """
        Click on the arrow button and open dropdown. Then choose folder/value from the list.
        :param dropdown:(str) the tuple of arrow button on dropdown
        :param list:(array []) the list of dropdown menu(path).
        Example: folder-folder-value ['Network Access', 'Authentication Status', 'AuthenticationPassed']
        """
        dropdown_list = ('CSS_SELECTOR', '.dijitPopup .xwtobjectselectorlist [dojoattachpoint="osItemNode"]')
        token_loader = ('CSS_SELECTOR', '[class="xwtOSWaitIndicator"] img[style*="display: block;"]')
        token_panel = ('CSS_SELECTOR', '.dijitPopup .dijitVisible[role="tabpanel"]')
        self.click_to(dropdown)
        for one in list:
            for dropdown_elem in Element(self.driver, dropdown_list)(multiple=True, implicitly_timeout=2):
                if one.lower() in dropdown_elem.text.lower():

                    if not one == list[-1]:
                        self.action.click(dropdown_elem.find_element_by_css_selector('[id="osItemNavNode"]'))
                        self.action.handle_loader(token_loader, time_appear=4)
                    else:
                        self.action.click(dropdown_elem)
                        self.waits.wait_for_web_element_not_visible(token_panel, timeout=3, raise_exception=False)
                        return
                    break
        raise FlowFailedException("Element is absent. Check test data")

    @staticmethod
    def is_last_option(option):
        """check if current option is last in
        the chain of options"""
        return '_flag' in option

    @staticmethod
    def add_flag(option):
        """add flag '_flag' to option text
        that is final in the chain of options"""
        return option + '_flag'

    def get_options(self, options):
        """Read received dict value from argument and
        create text list of options. If option is last in a list (final item),
        then add to this option text flag '_flag'.
        return list of options text"""
        list_of_options = []

        for key, value in options.items():
            if value:
                list_of_options.append(key)
                if isinstance(value, dict):
                    for k, val in value.items():
                        list_of_options.append(k)
                        list_of_options.append(self.add_flag(val))
                else:
                    list_of_options.append(self.add_flag(value))
            else:
                list_of_options.append(self.add_flag(key))
        return list_of_options

    def get_next_element_to_click(self, option):
        """return element to click (item or folder)
        that contains text of next option from a options list,
         and return element`s text"""
        if not self.action.check_is_element_present_in_dom(self.popup_repeater_dropdown_container_list,
                                                           timeout=10):
            raise FlowFailedException("No data present in a object selector window."
                                      "Failed to select following item : '{}'"
                                      .format(option.split('_')[0]))

        self.waits.wait_for_web_element_visible(self.popup_repeater_dropdown_container_list)
        for element in self.popup_repeater_dropdown_container_list(multiple=True):
            if option.split('_')[0] in element.text:
                return element, option

        raise FlowFailedException("No element (folder/item) found in a list"
                                  "of folders/items in object selector window,"
                                  "that contains text '{}'".format(option.split('_')[0]))

    def set_option(self, option, wait_panel_closed, wait_time):
        """perform click on element in object selector panel,
        that contains option text"""
        element, text = self.get_next_element_to_click(option)
        if self.is_last_option(text):
            self.action.click(element)
            if wait_panel_closed:
                self.waits.wait_for_web_element_not_visible(self.object_selector_panel,
                                                            raise_exception=True)
        else:
            try:
                self.action.click(element.find_element_by_css_selector("[id ='osItemNavNode']"))

            except WebDriverException as ex:
                if 'unknown error' in str(ex):
                    self.action.click(element)
                else:
                    raise SeleniumException("Can't click on element %s" % element)
            self.wait_token_panel_loaded(wait_time, 30)

    def navigate_to_initial_page(self):
        """
        Navigate to initial page,
        checks if there are any opened additional tabs
        in the browser, if so, switch to the first
        browser window which is initial page,
        trigger initial page navigate_to_page method
        """
        if len(self.driver.window_handles) > 1:
            self.action.switch_to_window(0)
            self.navigate_to_page()
        else:
            self.navigate_to_page()
        self.run_validations()

    def check_locator(self, locator, exception_message=''):
        """
         Check if element by specified locator is present.
         :param locator (tuple) locator of element to check
         :param exception_message (str) additional message in exception body
        """
        if not self.action.check_is_element_present_in_dom(locator, timeout=10):
            raise FlowFailedException(
                "No elements by locator : '{}' present on page. {}"
                .format(locator, exception_message))

    def close_session_info_toaster(self, time_to_wait=1):
        """check if session_info toaster present on page.
        And close."""
        toaster_pop_up = ("CSS_SELECTOR", ".xwtToaster[style*='block']")
        toaster_pop_up_close_btn = ("CSS_SELECTOR", ".xwtToaster[style*='block'] .xwtCloseIcon")
        LOGGER.info('Checking if session info pop up present')
        if self.action.check_is_element_present_in_dom(toaster_pop_up, timeout=time_to_wait):
            LOGGER.info('Found session info pop up on page')
            if self.waits.wait_for_web_element_visible(toaster_pop_up_close_btn, raise_exception=False):
                self.action.click(toaster_pop_up_close_btn)
                LOGGER.info('Closed session info pop up')
