import unittest
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

from fixtures.base_fixture import BaseFixture
from fixtures.create_work_order_fixture import WorkOrderFixture
from fixtures.login_fixture import LogInFixture


class TestCreateWorkOrder(LogInFixture, WorkOrderFixture):

    def test_Create_Work_Order_with_all_info(self) -> None:
        super().login("demo@oxmaint.com", "123456")
        super().create_work_order_with_all_info()

    def test_Create_Work_Order_with_required_info(self) -> None:
        super().login("demo@oxmaint.com", "123456")
        super().create_work_order_with_required_info(1)

    def test_Create_Work_Order_User_Able_To_Create_As_Much_Tasks_As_They_Want(self) -> None:
        super().login("demo@oxmaint.com", "123456")
        super().create_work_order_with_required_info(1)

if __name__ == '__main__':
    unittest.main()


