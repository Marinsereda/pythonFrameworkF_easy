import time

from base.session.session_decorator import SessionDecorators


class TestNetworkDevices:

    # @SessionDecorators.common_section()
    # def common_setup(self, *args):
    #     """"""
    #     print('here goes common setup section')
    #     time.sleep(2)


    @SessionDecorators.start()
    def setup_method(self, *args):
        """"""
        print('here goes setup')

    def test_some_test_file(self):
        self.session.logger.info('Test logger from test')
        time.sleep(2)


    @SessionDecorators.stop()
    def cleanup_method(self, *args):
        """"""
        print('here goes teardown')


    # @SessionDecorators.common_section()
    # def common_cleanup(self, *args):
    #     """"""
    #     print('here goes common cleanup section')
    #     time.sleep(2)


if __name__ == '__main__':
    Test = TestNetworkDevices()
    # Test.common_setup()

    Test.setup_method()
    Test.test_some_test_file()
    Test.cleanup_method()

    # Test.common_cleanup()