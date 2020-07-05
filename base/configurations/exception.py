"""Describes module with framework exceptions."""

from selenium.common.exceptions import WebDriverException


class CustomException(WebDriverException):
    """Describes custom framework exceptions"""

    def __init__(self, msg):
        super().__init__(msg)

class PageNotLoadedException(CustomException):
    """Raises in case if page is not loaded"""
    pass

class LoginPageNotLoadedException(CustomException):
    """Raises in case if login page is not loaded"""
    pass

class HomePageNotLoadedException(CustomException):
    """Raises in case if login page is not loaded"""
    pass

class SiteIsDeadException(CustomException):
    """Raises in case if login page is not loaded"""
    pass

class FlowFailedException(CustomException):
    """Raise if condition not met"""
    pass

class UnExpectedException(CustomException):
    """Raise if condition not met"""
    pass

class ElementNotFoundExcepiton(CustomException):
    """Raise if selenium element not found on a page"""
    pass

class ElementNotVisibleExcepiton(CustomException):
    """Raise if selenium element not found on a page"""
    pass

class ElementIsDisabledException(CustomException):
    """Raise if element is disabled"""
    pass

class ElementNotAvailableException(CustomException):
    """Raise if element is disabled"""
    pass

class AttributeNotFoundException(CustomException):
    """Raise if element is disabled"""
    pass
