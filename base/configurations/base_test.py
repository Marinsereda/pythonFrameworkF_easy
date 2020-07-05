from base.session.selenium_session import SeleniumSession
from base.configurations.logger import Logger
LOGGER = Logger(__name__).logger


class BaseTest:

    def init_session(self, browser='chrome', url=None, credentials=None):
        self.session = SeleniumSession(logger=LOGGER, browser=browser, url=url, credentials=credentials)

    def cleanup_session(self):
        if self.session:
            LOGGER.info("Stopping selenium session")
            self.session.driver.quit()
            delattr(self, 'session')