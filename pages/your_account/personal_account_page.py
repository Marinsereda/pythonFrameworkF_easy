from base.configurations.element import Element
from base.configurations.exception import LoginPageNotLoadedException
from pages.login_page import LoginPage
from components.calendar import Calendar


class PersonalAccountPage(LoginPage):
    """Describes Home page ->  Personal account page."""
    def __init__(self, session, make_login=True, navigate=True):
        super().__init__(session, make_login=make_login)
        if navigate:
            self.navigate_to_personal_accounts_page()

        self.calendar = Calendar(session=session)

    # page actions________________________________________________________

    def fill_email_confirm_input(self, text):
        self.action.send_keys(self.email_confirm_input, text)

    # page utils________________________________________________________
    def navigate_to_personal_accounts_page(self):
        self.logger.info("navigating to Personal accounts page")
        self.navigate_to_home_page_from_content()
        self.waits.wait_for_web_element_visible(self.open_user_account_button)
        self.action.click(self.open_user_account_button)
        self.waits.wait_for_web_element_visible(self.personal_room_button)
        self.action.click(self.personal_room_button)
        if not self.action.is_elements_present(self.profile_content_container, timeout=20):
            raise LoginPageNotLoadedException('PersonalAccountPage page was not loaded. Waited for 20 seconds ')

    # page locators________________________________________________________

    @property
    def open_user_account_button(self): return Element(self.session, ("CSS_SELECTOR", "#profile-menu-trigger--content"))
    @property
    def personal_room_button(self): return Element(self.session, ("CSS_SELECTOR", ".profile-menu__item"))
    @property
    def profile_content_container(self): return Element(self.session, ("CSS_SELECTOR", ".profile-area__content-container"))
    @property
    def email_confirm_input(self): return Element(self.session, ("CSS_SELECTOR", ".email-confirm-banner__email-text"))
    @property
    def checkin_expander(self): return Element(self.session, ("CSS_SELECTOR", '[data-mode="checkin"]'))
    @property
    def calendar_body(self): return Element(self.session, ("CSS_SELECTOR", ".c2-calendar-body"))


    #


