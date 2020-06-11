"""Module for driver config"""
CONFIG = {

    'chrome': {
                'path_to_driver': '/Users/fomin/Documents/chromedriver',    #chromedriver path
                'settings': {
                    'name': "",
                    'w3c': False,
                    "browserName": "chrome",
                    "version": "",
                    "platform": "ANY",
                    "javascriptEnabled": True,
                    "args": [
                        "--no-sandbox",
                        "--disable-extensions",
                        "--start-maximized",
                        "--ignore-certificate-errors",
                        "--allow-running-insecure-content",
                        "--start-fullscreen",
                        "--viewPort",
                        "--kiosk",
                        "--no-default-browser-check"
                    ]},
    },
    'firefox': {
                'path_to_driver': '/Users/fomin/Documents/geckodriver',     #gecko driver path
                'settings': {
                    "browserName": "firefox",
                    "marionette": True,
                    "acceptInsecureCerts": True,
                    "args": [
                        "--no-sandbox",
                        "--disable-extensions",
                        "--start-maximized",
                        "--ignore-certificate-errors",
                        "--allow-running-insecure-content",
                        "--start-fullscreen",
                        "--viewPort",
                        "--kiosk",
                        "--no-default-browser-check"
                    ]},
    },

    'ie': {

                'path_to_driver': '',     #ie path
                'settings': {
                    "browserName": "internet explorer",
                    "version": "",
                    "platform": "WINDOWS",
                    "javascriptEnabled": True,
                }
    }
}
