from base.configurations.element import Element
from base.configurations.interactions import Interactions
from base.configurations.waits import Waits
from base.configurations.exception import HomePageNotLoadedException

class BasePage:

    def __init__(self, session):
        self.session = session
        self.driver = session.driver
        self.logger = session.logger
        self.action = Interactions(self.session)
        self.waits = Waits(self.session)

    def navigate_to_home_page_from_content(self):
        if not self.action.is_element_displayed(self.events_search_form):
            self.action.click(self.booking_home_logo)
            if not self.action.is_element_displayed(self.events_search_form, timeout=20):
                raise HomePageNotLoadedException('Failed to navigate to home page from content.')
        self.logger.info("Home page successfully loaded.")

    @property
    def booking_home_logo(self): return Element(self.session, ("CSS_SELECTOR", "#top #logo_no_globe_new_logo"))
    @property
    def events_search_form(self): return Element(self.session, ("CSS_SELECTOR", ".js-ds-layout-events-search-form"))
