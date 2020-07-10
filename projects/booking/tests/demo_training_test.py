from base.configurations.base_test import BaseTest
from projects.booking.pages.your_account.personal_account_page import PersonalAccountPage

# should launch with pytest

class TestDemo(BaseTest):

    # def test_login_page(self):
    #     self.init_session()
    #     LoginPage(self.session).login_to_booking()
    #     self.cleanup_session()


    def test_personal_accunts_page(self):
        self.init_session()
        page = PersonalAccountPage(session=self.session)
        page.fill_email_confirm_input('someemail@ukr.net')
        page.calendar.open_calendar(page.checkin_expander)
        page.calendar.select_date('2020', '07', '02')
        self.cleanup_session()

# marina changes
