import os
import unittest
import configparser

from APIs import remove_all_device_tags
from APIs import add_device_tag
from APIs import get_device_id
from APIs import finish_cleanup_state
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities

status = 'failed'

uid = os.getenv("deviceID")
os = os.getenv("deviceOS")

capabilities = DesiredCapabilities.IPHONE

config = configparser.ConfigParser()
config.read('config.properties')


class SampleTestCase(unittest.TestCase):

    # def test_2(self):
        # print(get_device_id('56793ec400fe2121df8a6341591cbd25b7c26c70'))

    capabilities['testName'] = 'pythonTest'
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
        device_id = get_device_id(device_udid)
        wifi_label = self.driver.find_element(By.XPATH, "(//*[@id='Wi-Fi']//XCUIElementTypeStaticText)[2]")

        # Check if the desired wifi name is present in the connected wifi
        if config.get('wifi', 'wifi_name') in wifi_label.text:
            print('Connected to correct WiFi: %s' % wifi_label.text)
            # remove all device tags
            remove_all_device_tags(device_id)
            # add custom device tag
            add_device_tag(device_id, config.get('tags', 'good_tag_value'))
        else:
            print('Not Connected to correct WiFi: %s' % wifi_label.text)
            # remove all device tags
            remove_all_device_tags(device_id)
            # add custom device tag
            add_device_tag(device_id, config.get('tags', 'bad_tag_value'))

    def tearDown(self):
        status = 'passed'
        self.driver.quit()
        finish_cleanup_state(uid, status)


runner = unittest.TextTestRunner()
suite = unittest.TestLoader().loadTestsFromTestCase(SampleTestCase)
