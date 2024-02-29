import unittest
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from fixtures.base_fixture import BaseFixture


class LogInFixture(BaseFixture):

    def login(self, email, password):
        time.sleep(3)
        self.driver.find_element(by=AppiumBy.ID, value='com.jrs.oxmaint:id/btn_continue').click()
        self.driver.find_element(by=AppiumBy.ID, value='com.jrs.oxmaint:id/btn_signup').click()

        while True:
            try:
                self.driver.find_element(by=AppiumBy.ID, value='com.jrs.oxmaint:id/btn_login').click()
            except NoSuchElementException or ElementClickInterceptedException:
                continue
            if self.wait.until(EC.element_to_be_clickable((By.ID, 'com.jrs.oxmaint:id/btn1'))).is_enabled():
                break

        self.driver.find_element(by=AppiumBy.XPATH,
                                 value='//android.widget.Button[@resource-id="com.jrs.oxmaint:id/btn1"]').click()

        # Fill email field
        self.driver.find_element(by=AppiumBy.ID, value='com.jrs.oxmaint:id/email').send_keys(email)
        # Fill password field
        self.driver.find_element(by=AppiumBy.ID, value='com.jrs.oxmaint:id/password').send_keys(password)
        # Click login
        self.driver.find_element(by=AppiumBy.ID, value='com.jrs.oxmaint:id/btn_login').click()

        try:
            self.driver.find_element(by=AppiumBy.ID,
                                     value='com.android.permissioncontroller:id/permission_allow_button').click()
        except NoSuchElementException:
            pass
