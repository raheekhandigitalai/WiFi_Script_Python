import os
import unittest
import configparser

from selenium.webdriver import DesiredCapabilities

from APIs import remove_all_device_tags
from APIs import add_device_tag
from APIs import get_device_id
from APIs import finish_cleanup_state
from appium import webdriver
from selenium.webdriver.common.by import By

access_key_admin = 'eyJ4cC51Ijo3MzU0MjQsInhwLnAiOjIsInhwLm0iOiJNVFUzT0RZd016ZzFOek16TVEiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE4OTM5NjM4NTcsImlzcyI6ImNvbS5leHBlcml0ZXN0In0.GP0hK0o0j2WEKt-J0aXsVbu1tmt-PhWUryqluokszJk'

wifi_name = "ECustomers_ALL_Legacy"
bad_tag_value = 'BadWiFi'
good_tag_value = 'GoodWiFi'

status = 'failed'

uid = os.getenv("deviceID")
# uid = '56793ec400fe2121df8a6341591cbd25b7c26c70'
os = os.getenv("deviceOS")

capabilities = DesiredCapabilities.IPHONE

config = configparser.ConfigParser()
config.read('config.properties')
# device_name = os.getenv("deviceName")
# os_version = os.getenv("osVersion")
# device_model = os.getenv("deviceModel")
# device_manufacturer = os.getenv("deviceManufacturer")
# device_category = os.getenv("deviceCategory")
# username = os.getenv("username")
# user_project = os.getenv("userProject")

# desired_caps = dict(
#     testName="PythonTest",
#     accessKey="eyJ4cC51Ijo3MzU0MjQsInhwLnAiOjIsInhwLm0iOiJNVFUzT0RZd016ZzFOek16TVEiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE4OTM5NjM4NTcsImlzcyI6ImNvbS5leHBlcml0ZXN0In0.GP0hK0o0j2WEKt-J0aXsVbu1tmt-PhWUryqluokszJk",
#     deviceQuery="@serialnumber='56793ec400fe2121df8a6341591cbd25b7c26c70'",
#     # deviceQuery="@serialnumber='%s'" % uid,
#     platformName="iOS",
#     autoDismissAlerts=True,
#     releaseDevice=False,
#     bundleId="com.apple.Preferences"
# )


class SampleTestCase(unittest.TestCase):

    # def test_2(self):
        # print(get_device_id('56793ec400fe2121df8a6341591cbd25b7c26c70'))

    capabilities['testName'] = 'pythonTest'
    # capabilities['accessKey'] = '%s' % config.get('seetest_authorization', 'access_key_admin')
    capabilities['accessKey'] = '%s' % config.get('seetest_authorization', 'access_key_cleanup')
    capabilities['udid'] = '%s' % uid
    capabilities['platformName'] = 'iOS'
    capabilities['autoDismissAlerts'] = True
    capabilities['releaseDevice'] = False
    capabilities['newCommandTimeout'] = 60
    capabilities['bundleId'] = 'com.apple.Preferences'

    def setUp(self):
        self.driver = webdriver.Remote(desired_capabilities=capabilities, command_executor='https://uscloud.experitest.com/wd/hub')

    def test_1(self):
        device_udid = self.driver.capabilities['udid']
        # device_udid = self.driver.caps['udid'] // works in selenium4 / appiumclient 2.1.0
        device_id = get_device_id(device_udid)
        wifi_label = self.driver.find_element(By.XPATH, "(//*[@id='Wi-Fi']//XCUIElementTypeStaticText)[2]")

        if wifi_name in wifi_label.text:
            print('found')
            # remove all device tags
            remove_all_device_tags(device_id)
            # add custom device tag
            add_device_tag(device_id, good_tag_value)
        else:
            print('not found')
            # remove all device tags
            remove_all_device_tags(device_id)
            # add custom device tag
            add_device_tag(device_id, bad_tag_value)

        status = 'passed'

    def tearDown(self):
        finish_cleanup_state(uid, status)
        print(status)
        self.driver.quit()


runner = unittest.TextTestRunner()
suite = unittest.TestLoader().loadTestsFromTestCase(SampleTestCase)
