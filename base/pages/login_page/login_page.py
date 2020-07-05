import time

from base.configurations.base_page import BasePage
from base.configurations.element import Element
from base.configurations.exception import LoginPageNotLoadedException, \
    HomePageNotLoadedException


class LoginPage(BasePage):
    """Describes Base Page Element. And common methods for all page objects"""
    def __init__(self, session):
        self.email_for_login = session.credentials[0]
        self.password_for_login = session.credentials[1]
        super().__init__(session, make_login=False)

    # page actions________________________________________________________

    def navigate_to_login_page(self, login_page_init_time=60):
        self.driver.get(self.session.url)
        if not self.action.is_elements_present(self.main_form_container, timeout=login_page_init_time):
            raise LoginPageNotLoadedException('Login page was not loaded. Waited for {} seconds '.format(login_page_init_time))

    def click_enter_in_account(self):
        self.waits.wait_for_web_element_visible(self.enter_in_account_btn)
        self.action.click(self.enter_in_account_btn)

    def fill_in_email(self, text_to_send):
        self.waits.wait_for_web_element_visible(self.email_input)
        self.action.send_keys(self.email_input, text_to_send)

    def click_next_button(self):
        self.waits.wait_for_web_element_visible(self.next_button)
        self.action.click(self.next_button)

    def fill_in_password(self, text_to_send):
        self.waits.wait_for_web_element_visible(self.password_input)
        self.action.send_keys(self.password_input, text_to_send)

    def submit_login(self, wait_for_home_page=True, wait_time=60):
        self.waits.wait_for_web_element_visible(self.submit_login_button)
        self.action.click(self.submit_login_button)
        if wait_for_home_page:
            if not self.action.is_elements_present(self.my_profile_button, timeout=wait_time):
                raise HomePageNotLoadedException('Home page was not loaded. Waited for {} seconds'.format(wait_time))


    # page utils________________________________________________________

    def handle_welcome_pop_up(self):
        """ close "Добро пожаловать... как вас зовут ..." """
        if self.action.is_element_displayed(self.close_welcome_modal_button):
            self.action.click(self.close_welcome_modal_button)
            self.waits.wait_for_web_element_not_visible(self.close_welcome_modal_button)

    def navigate_to_home_page_from_content(self):
        if not self.action.is_element_displayed(self.events_search_form):
            self.action.click(self.booking_home_logo)
            if not self.action.is_element_displayed(self.events_search_form, timeout=20):
                raise HomePageNotLoadedException('Failed to navigate to home page from content.')
        self.logger.info("Home page successfully loaded.")

    def login_to_booking(self):
        self.navigate_to_login_page()
        self.click_enter_in_account()
        self.fill_in_email(self.email_for_login)
        self.click_next_button()
        self.fill_in_password(self.password_for_login)
        self.submit_login()
        self.handle_welcome_pop_up()
        self.navigate_to_home_page_from_content()


    # page locators________________________________________________________

    @property
    def main_form_container(self): return Element(self.session, ("CSS_SELECTOR", "#bodyconstraint-inner"))
    @property
    def enter_in_account_btn(self): return Element(self.session, ("CSS_SELECTOR", ".account_register_option span"))
    @property
    def email_input(self): return Element(self.session, ("CSS_SELECTOR", 'input[id="username"]'))
    @property
    def next_button(self):return Element(self.session, ("CSS_SELECTOR", '.transition button[type="submit"]'))
    @property
    def password_input(self): return Element(self.session, ("CSS_SELECTOR", 'input#password'))
    @property
    def submit_login_button(self): return Element(self.session, ("CSS_SELECTOR", 'button[type="submit"]'))
    @property
    def my_profile_button(self): return Element(self.session, ("CSS_SELECTOR", '[id="profile-menu-trigger--content"]'))
    @property
    def close_welcome_modal_button(self): return Element(self.session, ("CSS_SELECTOR", ".modal-mask-closeBtn"))
    @property
    def booking_home_logo(self): return Element(self.session, ("CSS_SELECTOR", "#top #logo_no_globe_new_logo"))
    @property
    def events_search_form(self): return Element(self.session, ("CSS_SELECTOR", ".js-ds-layout-events-search-form"))




