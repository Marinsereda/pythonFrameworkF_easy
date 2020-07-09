import time
from base.configurations.base_page import BasePage
from base.configurations.element import Element
from base.configurations.exception import FlowFailedException


class Calendar(BasePage):
    """Describes actions with calendar."""

    # actions________________________________________________________

    def open_calendar(self, expand_element):
        self.action.click(expand_element)
        self.waits.wait_for_web_element_visible(self.calendar_body)

    def click_next_month(self):
        """click next month button"""
        self.action.click(self.calendar_next)
        time.sleep(3)

    def click_previous_month(self):
        """click next month button"""
        self.action.click(self.calendar_previous)
        time.sleep(3)

    def select_date(self, year, month, day):
        self.select_date_from_calendar(year, month, day)


    # utils________________________________________________________

    def select_date_from_calendar(self, year, month, day):
        """e.g. year = 2020 , month =  07  , day 01"""
        date = "{}-{}-{}".format(year, month, day)
        self.logger.info('Selecting following date from the calendar: {}'.format(date))
        date_locator = ("CSS_SELECTOR", "td.bui-calendar__date[data-date='{}']".format(date))
        if not self.action.is_element_displayed(date_locator):
            raise FlowFailedException("Date not found or not visible in calendar. Locator {}".format(date_locator))
        else:
            self.action.click(date_locator)



    # locators________________________________________________________

    @property
    def calendar_body(self): return Element(self.session, ("CSS_SELECTOR", ".bui-calendar[style*='block']"))
    @property
    def calendar_next(self): return Element(self.session, ("CSS_SELECTOR", ".bui-calendar__control--next"))
    @property
    def calendar_previous(self): return Element(self.session, ("CSS_SELECTOR", '.bui-calendar__control--prev"]'))
    @property
    def calendar_active_date(self):return Element(self.session, ("CSS_SELECTOR", 'td.bui-calendar__date[data-date]'))

    # @property
    # def password_input(self): return Element(self.session, ("CSS_SELECTOR", 'input#password'))
    # @property
    # def submit_login_button(self): return Element(self.session, ("CSS_SELECTOR", 'button[type="submit"]'))
    # @property
    # def my_profile_button(self): return Element(self.session, ("CSS_SELECTOR", '[id="profile-menu-trigger--content"]'))
    # @property
    # def close_welcome_modal_button(self): return Element(self.session, ("CSS_SELECTOR", ".modal-mask-closeBtn"))




