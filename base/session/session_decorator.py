from base.configurations.logger import Logger
# LOGGER = Logger.create_logger(__name__)
import os
import re
import sys
import time
import inspect
from functools import wraps
import requests
from urllib3.exceptions import MaxRetryError
from base.session.selenium_session import SeleniumSession
import configparser
import os

from base.configurations.logger import Logger
LOGGER = Logger(__name__).logger

session_name = 'session'
path_to_default_config = (os.path.dirname(os.path.realpath(__file__)) + "/../configs/default_config.ini")
DEFAULT_CONFIG = configparser.ConfigParser()
DEFAULT_CONFIG.read(path_to_default_config)






class SessionDecorators:
    """
    Module for session decorators
    Contains static and stop methods to use as decorator for setup and
     teardown testcases
    """

    @staticmethod
    def start(browser="chrome"):
        """start session decorator"""

        def wrap(passed_f):
            def wrapped_f(*args, **kwargs):
                test_class = args[0]
                session_instance = SeleniumSession(config=DEFAULT_CONFIG, browser=browser, logger=LOGGER)
                setattr(test_class, session_name, session_instance)
                passed_f(*args, **kwargs)
            return wrapped_f
        return wrap

    @staticmethod
    def stop():
        """stop session decorator"""
        def wrap(passed_f):
            def wrapped_f(*args, **kwargs):
                LOGGER.info("should stop the session now")
                try:
                    test_class = args[0]
                    getattr(test_class, session_name).driver.quit()
                    delattr(test_class, session_name)
                    # cfg.zalenium.stop_zalenium_associated_container()
                except Exception as excep:
                    LOGGER.info('During teardown_method faced following exception:' + str(excep))
                passed_f(*args, **kwargs)
            return wrapped_f
        return wrap

    @staticmethod
    def common_section(browser="chrome"):
        """Used to decorate common setup/ common cleanup sections.
        Start session before and stop session after """


        def wrap(passed_f):

            def wrapped_f(*args, **kwargs):
                test_class = args[0]
                session_instance = SeleniumSession(config=DEFAULT_CONFIG, browser=browser, logger=LOGGER)
                setattr(test_class, session_name, session_instance)
                try:
                    passed_f(*args, **kwargs)
                except Exception as exception:
                    raise exception
                finally:
                    LOGGER.info("should stop the session now")
                    getattr(test_class, session_name).driver.quit()
                    delattr(test_class, session_name)

            return wrapped_f

        return wrap

 #    def decorate(cls):
 #        """
 #        Running before TestSuite. Write decorator and default setup/teardown methods
 #        :param cls:  TestSuite
 #        """
 #
 #        for attr in cls.__dict__:
 #            method_obj = getattr(cls, attr)
 #            if callable(method_obj):
 #
 #                getsource = inspect.getsource(method_obj)
 #                if '@aetest.' not in getsource:
 #                    if session_up:
 #                        setattr(cls, attr, decorator_aetest_subsection(
 #                            decorator_retry(decorator_iseac_start(decorator_iseac_stop(method_obj)))))
 #                    else:
 #                        setattr(cls, attr, decorator_aetest_subsection(decorator_retry_session_down(method_obj)))
 #
 #        return cls
 #
 #    return decorate
 #
 #
 #
 # @staticmethod
 #    def common_section(browser="chrome"):
 #        """Used to decorate common setup/ common cleanup sections.
 #        Start session before and stop session after """
 #
 #        decorator_session_start = SessionDecorators.start(browser=browser)
 #        decorator_session_stop = SessionDecorators.stop(common=True)
 #
 #        def wrap(passed_f):
 #            @wraps(passed_f)
 #            def wrapped_f(*args, **kwargs):
 #                # name_of_method = passed_f.__name__
 #                decorator_session_start(decorator_session_stop(passed_f(*args, **kwargs)))
 #
 #            return wrapped_f
 #
 #        return wrap