from base.configurations.base_test import BaseTest
from pages.login_page import LoginPage
from pages.your_account.personal_account_page import PersonalAccountPage


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

    # @SessionDecorators.common_section()
    # def common_setup(self, *args):
    #     """"""
    #     print('here goes common setup section')
    #     time.sleep(2)


    # @SessionDecorators.start()
    # def setup_method(self, *args):
    #     """"""
    #     print('here goes setup')
    #
    # def test_some_test_file(self):
    #     self.session.logger.info('Test logger from test')
    #     time.sleep(2)
    #
    #
    # @SessionDecorators.stop()
    # def cleanup_method(self, *args):
    #     """"""
    #     print('here goes teardown')


    # @SessionDecorators.common_section()
    # def common_cleanup(self, *args):
    #     """"""
    #     print('here goes common cleanup section')
    #     time.sleep(2)


# if __name__ == '__main__':
#     Test = TestNetworkDevices()
#     # Test.common_setup()
#
#     Test.setup_method()
#     Test.test_some_test_file()
#     Test.cleanup_method()

    # Test.common_cleanup()