from base.configurations.base_test import BaseTest
from projects.booking.pages.your_account.personal_account_page import PersonalAccountPage
from projects.booking.pages.setting_page import SettingPage
from base.configurations.interactions import Interactions as actions
from base.configurations.element import Element

# should launch with pytest

class TestDemo(BaseTest):

    # def test_login_page(self):
    #     self.init_session()
    #     LoginPage(self.session).login_to_booking()
    #     self.cleanup_session()

    # def test_personal_accunts_page(self):
    #     self.init_session()
    #     page = PersonalAccountPage(session=self.session)
    #     page.fill_email_confirm_input('someemail@ukr.net')
    #     page.calendar.open_calendar(page.checkin_expander)
    #     page.calendar.select_date('2020', '07', '02')
    #     self.cleanup_session()

    def test_setting_page(self):
        self.init_session()
        setting = SettingPage(session=self.session)
        setting.navigate_to_settings()
        setting.edit_personal_info("DeFault Name", "3", "April", "2000", "USA")


