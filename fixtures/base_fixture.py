import unittest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait


capabilities = dict(
    platformName='Android',
    automationName= 'uiautomator2',
    deviceName= 'Android',
    appPackage= 'com.jrs.oxmaint',
    appActivity='com.jrs.oxmaint.login.Splash',
    language= 'en',
    locale= 'US'
)

appium_server_url = "http://localhost:4723"

class BaseFixture(unittest.TestCase):

    def setUp(self) -> None:

        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
        self.wait = WebDriverWait(self.driver, 15)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()