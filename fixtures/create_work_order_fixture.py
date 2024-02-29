import unittest
import time
from datetime import datetime, timedelta

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from fixtures.base_fixture import BaseFixture
from fixtures.login_fixture import LogInFixture
from faker import Faker
from selenium.webdriver.support import expected_conditions as EC

fake = Faker()

date_format = "%d-%b-%Y %I:%M %p"



class WorkOrderFixture(BaseFixture):

    def create_work_order_with_required_info(self, tasks_amount=1) -> None:
        self.title = fake.name()
        self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                    '//android.widget.LinearLayout[@resource-id="com.jrs.oxmaint:id/btn_wo_3"]/android.widget.ImageView'))).click()
        self.wait.until(EC.presence_of_element_located((By.ID, 'com.jrs.oxmaint:id/fab'))).click()

        # Add title
        self.wait.until(EC.presence_of_element_located((By.ID, 'com.jrs.oxmaint:id/et_wo_title')))
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et_wo_title').send_keys(self.title)

        # Save Work Order Number
        self.work_order_number = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.jrs.oxmaint:id/view_wo_number'))).text

        # Select Asset
        self.driver.find_element(by=By.XPATH, value='(//android.widget.TextView[@text="Select"])[1]').click()
        self.asset_number = self.wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView['
                                                                                      '@resource-id="com.jrs.oxmaint:id/tv1"])[1]'))).text
        self.driver.find_element(by=By.XPATH,
                                 value='(//android.widget.TextView[@resource-id="com.jrs.oxmaint:id/select"])[1]').click()

        # Add Task
        for i in range(tasks_amount):
            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/add_task_btn').click()
            self.wait.until(EC.presence_of_element_located((By.ID, 'com.jrs.oxmaint:id/task_name')))
            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/task_name').send_keys("Some Task")
            self.driver.find_element(by=By.ID, value='android:id/button1').click()
            time.sleep(1)

        # Click Create Work Order
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/insert_btn').click()

        # Writing down creation time
        # ///
        current_datetime = datetime.now()
        time_minus_one_minute = current_datetime - timedelta(minutes=1)
        time_plus_one_minute = current_datetime + timedelta(minutes=1)

        self.formatted_time_minus_one_minute = time_minus_one_minute.strftime(date_format)
        self.formatted_time_plus_one_minute = time_plus_one_minute.strftime(date_format)
        self.formatted_date = current_datetime.strftime(date_format)
        # ///

        # If message about storage
        message = self.driver.find_element(by=By.ID, value='android:id/button1')
        if message:
            message.click()
            self.driver.find_element(by=By.ID,
                                     value='com.android.permissioncontroller:id/permission_allow_button').click()

        # Success message
        self.wait.until(EC.element_to_be_clickable((By.ID, 'android:id/button2'))).click()

        assert self.driver.find_element(by=By.XPATH, value='(//android.widget.TextView['
                                                           '@resource-id="com.jrs.oxmaint:id/tv_wo_number"])['
                                                           '1]').text == self.work_order_number

        assert self.driver.find_element(by=By.XPATH,
                                        value='(//android.widget.TextView[@resource-id="com.jrs.oxmaint:id/tv_title"])[1]').text == self.title

        assert self.driver.find_element(by=By.XPATH,
                                        value='(//android.widget.TextView[@resource-id="com.jrs.oxmaint:id/tv_vehicle"])[1]').text == self.asset_number

        self.created_time = self.driver.find_element(by=By.XPATH,
                                                     value='(//android.widget.TextView[@resource-id="com.jrs.oxmaint:id/tv_created"])[1]').text
        assert (self.created_time == self.formatted_date or
                self.created_time == self.formatted_time_minus_one_minute or
                self.created_time == self.formatted_time_plus_one_minute)

    def create_work_order_with_all_info(self, tasks_amount=1, labors_amount=1, additional_cost_amount=1, remarks_amount=1, attachments_amount=1) -> None:
        self.a2 = TouchAction(self.driver)
        self.memo = fake.text()
        self.title = fake.name()
        self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                    '//android.widget.LinearLayout[@resource-id="com.jrs.oxmaint:id/btn_wo_3"]/android.widget.ImageView'))).click()

        # Add title
        self.wait.until(EC.presence_of_element_located((By.ID, 'com.jrs.oxmaint:id/fab'))).click()
        self.wait.until(EC.presence_of_element_located((By.ID, 'com.jrs.oxmaint:id/et_wo_title')))
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et_wo_title').send_keys(self.title)

        # Save Work Order Number
        self.work_order_number = self.wait.until(
            EC.presence_of_element_located((By.ID, 'com.jrs.oxmaint:id/view_wo_number'))).text

        # Select Asset
        self.driver.find_element(by=By.XPATH, value='(//android.widget.TextView[@text="Select"])[1]').click()
        self.asset_number = self.wait.until(EC.presence_of_element_located((By.XPATH, '(//android.widget.TextView['
                                                                                      '@resource-id="com.jrs.oxmaint:id/tv1"])[1]'))).text
        self.driver.find_element(by=By.XPATH,
                                 value='(//android.widget.TextView[@resource-id="com.jrs.oxmaint:id/select"])[1]').click()

        # Add Task
        for i in range(tasks_amount):
            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/add_task_btn').click()
            self.wait.until(EC.presence_of_element_located((By.ID, 'com.jrs.oxmaint:id/task_name')))
            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/task_name').send_keys("Some Task")
            self.driver.find_element(by=By.ID, value='android:id/button1').click()
            time.sleep(1)


        # Add memo
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et_wo_memo').send_keys(self.memo)

        # Assign to
        self.driver.find_element(by=By.XPATH, value='(//android.widget.TextView[@text="Select"])[2]').click()
        self.driver.find_element(by=By.XPATH, value='(//androidx.recyclerview.widget.RecyclerView[@resource-id="com.jrs.oxmaint:id/list"]/android.widget.LinearLayout)[1]').click()
        self.assign_to = self.driver.find_element(by=By.XPATH, value='(//androidx.recyclerview.widget.RecyclerView[@resource-id="com.jrs.oxmaint:id/list"]/android.widget.LinearLayout)[1]').text
        self.driver.find_element(by=By.ID, value='android:id/button1').click()

        # Due date
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/due_date').click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'android:id/button1'))).click()
        self.driver.find_element(by=By.ID, value='android:id/button1').click()

        # Additional details
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/additional_collapse').click()

        # Start date
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/start_date').click()
        self.driver.find_element(by=By.ID, value='android:id/button1').click()
        self.driver.find_element(by=By.ID, value='android:id/button1').click()

        # Estimated cost
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/estimated_cost').send_keys(123)

        # Estimated labor time
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/estimated_time').send_keys(123)

        # Scroll down
        self.size = self.driver.get_window_size()
        self.startY = self.size['height'] * 0.80
        self.endY = self.size['height'] * 0.20
        self.startX = self.size['width'] / 2
        self.driver.swipe(self.startX, self.startY, self.startX, self.endY, 3000)

        # Link Inspection
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/select_link_inspection').click()
        self.wait.until(EC.presence_of_element_located((By.ID, 'com.jrs.oxmaint:id/action'))).click()

        # Link WorkOrder
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/select_link_wo').click()
        self.driver.find_element(by=By.XPATH, value='(//android.widget.ImageView[@resource-id="com.jrs.oxmaint:id/action"])[1]').click()

        # !!!BUG!!! Can't enter any data into Cost Detail
        # # Expand Cost Detail
        # self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/cost_collapse').click()


        # Add Labor
        for i in range(labors_amount):
            self.driver.find_element(by=By.XPATH, value='//android.widget.TextView[@text="Labor"]').click()
            self.wait.until(EC.element_to_be_clickable((By.ID, 'com.jrs.oxmaint:id/add_labor_btn'))).click()
            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/select').click()
            self.driver.find_element(by=By.XPATH, value='//android.widget.TextView[@resource-id="com.jrs.oxmaint:id/tv1" and @text="gaurav01"]').click()
            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/select_code').click()
            self.driver.find_element(by=By.XPATH, value='//androidx.recyclerview.widget.RecyclerView[@resource-id="com.jrs.oxmaint:id/list"]/android.widget.LinearLayout[1]').click()

            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et4').send_keys(123)

            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et5').send_keys(123)

            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et6').send_keys("Some Note")

            self.driver.find_element(by=By.ID, value='android:id/button1').click()
            time.sleep(1)

        # Add Additional Cost
        for i in range(additional_cost_amount):
            self.driver.find_element(by=By.XPATH, value='//android.widget.TextView[@text="Additional Cost"]').click()
            self.wait.until(EC.element_to_be_clickable((By.ID, 'com.jrs.oxmaint:id/add_cost_btn'))).click()
            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et1').send_keys("Some Description")
            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et2').send_keys(123)
            self.driver.find_element(by=By.ID, value='android:id/button1').click()
            time.sleep(1)

        # Add Remark
        for i in range(remarks_amount):
            self.driver.find_element(by=By.XPATH, value='//android.widget.TextView[@text="Remarks"]').click()
            self.wait.until(EC.element_to_be_clickable((By.ID, 'com.jrs.oxmaint:id/add_remark_btn'))).click()
            self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et1').send_keys("Some Remark")
            self.driver.find_element(by=By.ID, value='android:id/button1').click()
            time.sleep(1)

        # !!!BUG!!! Can't attach any pictures
        # # Add Attachments
        # for i in range(attachments_amount):
            # self.driver.find_element(by=By.XPATH, value='//android.widget.TextView[@text="Attachments"]').click()
            # self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/add_attachment_btn').click()
            # self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/et1').send_keys("Some Description for Attachment")
            # self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/select').click()
            # self.driver.find_element(by=By.XPATH, value='//android.widget.TextView[@resource-id="android:id/text1" and @text="Take a Picture"]').click()
            # self.driver.find_element(by=By.ID, value='android:id/button1').click()
            # self.driver.find_element(by=By.ID, value='com.android.permissioncontroller:id/permission_allow_foreground_only_button').click()
            # self.driver.find_element(by=By.ID, value='com.android.camera2:id/shutter_button').click()
            # time.sleep(2)

        # Click Create Work Order
        self.driver.find_element(by=By.ID, value='com.jrs.oxmaint:id/insert_btn').click()

        # Writing down creation time
        # ///
        current_datetime = datetime.now()
        time_minus_one_minute = current_datetime - timedelta(minutes=1)
        time_plus_one_minute = current_datetime + timedelta(minutes=1)

        self.formatted_time_minus_one_minute = time_minus_one_minute.strftime(date_format)
        self.formatted_time_plus_one_minute = time_plus_one_minute.strftime(date_format)
        self.formatted_date = current_datetime.strftime(date_format)
        # ///

        # If message about storage
        message = self.driver.find_element(by=By.ID, value='android:id/button1')
        if message:
            message.click()
            self.wait.until(EC.element_to_be_clickable((By.ID, 'com.android.permissioncontroller:id/permission_allow_button'))).click()

        # Success message
        self.wait.until(EC.element_to_be_clickable((By.ID, 'android:id/button2'))).click()

        assert self.driver.find_element(by=By.XPATH, value='(//android.widget.TextView['
                                                           '@resource-id="com.jrs.oxmaint:id/tv_wo_number"])['
                                                           '1]').text == self.work_order_number

        assert self.driver.find_element(by=By.XPATH,
                                        value='(//android.widget.TextView[@resource-id="com.jrs.oxmaint:id/tv_title"])[1]').text == self.title

        assert self.driver.find_element(by=By.XPATH,
                                        value='(//android.widget.TextView[@resource-id="com.jrs.oxmaint:id/tv_vehicle"])[1]').text == self.asset_number

        self.created_time = self.driver.find_element(by=By.XPATH,
                                                     value='(//android.widget.TextView[@resource-id="com.jrs.oxmaint:id/tv_created"])[1]').text
        assert (self.created_time == self.formatted_date or
                self.created_time == self.formatted_time_minus_one_minute or
                self.created_time == self.formatted_time_plus_one_minute)









