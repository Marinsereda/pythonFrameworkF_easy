import time
from base.configurations.base_page import BasePage
from base.configurations.element import Element
from base.configurations.exception import LoginPageNotLoadedException, \
    HomePageNotLoadedException
from projects.booking.pages.login_page import LoginPage



class SettingPage(LoginPage):
    """Describes Settings Page Element. And common methods for all page objects"""
    def __init__(self, session, make_login=True, navigate=True):
        super().__init__(session, make_login=make_login)
        if navigate:
            self.navigate_to_login_page()

    def navigate_to_login_page(self, login_page_init_time=60):
        self.logger.info('navigating to login page by address: {}'.format(self.session.url))
        self.driver.get(self.session.url)
        if not self.action.is_elements_present(self.main_form_container, timeout=login_page_init_time):
            raise LoginPageNotLoadedException(
                'Login page was not loaded. Waited for {} seconds '.format(login_page_init_time))

    def navigate_to_settings(self):
        #open settings page
        self.logger.info('navigating to settings page by selector: {}'.format(self.navigate_to_account_menu()))
        self.action.click(self.navigate_to_account_menu)
        self.action.click(self.navigate_to_settings_page)

    def edit_personal_info(self, nickname="", bday="", bmonth="", byear="", country=""):
        self.logger.info('edit nickname input by selector: {}'.format(self.nickname_input))
        self.waits.wait_for_web_element_visible(self.nickname_input)
        self.action.send_keys(self.nickname_input, text_to_send=nickname)

        self.action.select_from_drop_down_by_text(
            list_of_options_from_dropdown=self.bday_drop_down,
        text_to_select=bday)
        # self.action.select_from_drop_down_by_text(
        #     list_of_options_from_dropdown=self.bmonth_drop_down,
        # text_to_select=bmonth)
        # self.action.select_from_drop_down_by_text(
        #     list_of_options_from_dropdown=self.byear_drop_down,
        # text_to_select=byear)
        # self.action.select_from_drop_down_by_text(
        #     list_of_options_from_dropdown=self.country_drop_down,
        # text_to_select=country)





    @property
    def navigate_to_account_menu(self):
        return Element(self.session, ("CSS_SELECTOR", "#current_account"))
    @property
    def navigate_to_settings_page(self):
        return Element(self.session, ("XPATH", "//*[@id='profile-menu']//*[contains(text(), 'Settings')]"))
    @property
    def nickname_input(self):
        return Element(self.session, ("CSS_SELECTOR", "input#nickname"))
    @property
    def bday_drop_down(self):
        return Element(self.session, ("CSS_SELECTOR", "select#bday"))
    @property
    def bmonth_drop_down(self):
        return Element(self.session, ("CSS_SELECTOR", "select#bmonth"))
    @property
    def byear_drop_down(self):
        return Element(self.session, ("CSS_SELECTOR", "select#byear"))
    @property
    def country_drop_down(self):
        return Element(self.session, ("CSS_SELECTOR", "select#nationality"))

