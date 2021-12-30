import os
import unittest
import configparser
import sys

from APIs import remove_all_device_tags
from APIs import add_device_tag
from APIs import get_device_id
from APIs import finish_cleanup_state
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import DesiredCapabilities

status = 'failed'

uid = os.getenv("deviceID")
operating_system = os.getenv("deviceOS")

# Pre-defining the iPhone capabilities as script is designed for iOS only for now
capabilities = DesiredCapabilities.IPHONE

# config.properties reader
config = configparser.ConfigParser()
config.read('config.properties')


# Re-usable method for logging purposes
def logger(content):
    print(content)


class SampleTestCase(unittest.TestCase):
    # def test_2(self):
    # print(get_device_id('56793ec400fe2121df8a6341591cbd25b7c26c70'))

    # Android currently not supported. If Device is Android, exit the script before it starts
    if operating_system == 'Android':
        logger('operating_system is android, not yet supported: %s' % operating_system)
        status = 'passed'
        finish_cleanup_state(uid, status)
        sys.exit()
    elif operating_system == 'iOS':
        logger('operating_system is ios, continuing: %s' % operating_system)

    capabilities['testName'] = 'Webhook cleanup'
    capabilities['accessKey'] = '%s' % config.get('seetest_authorization', 'access_key_cleanup')
    capabilities['udid'] = '%s' % uid
    capabilities['platformName'] = 'iOS'
    capabilities['autoDismissAlerts'] = True
    capabilities['releaseDevice'] = False
    capabilities['bundleId'] = 'com.apple.Preferences'

    def setUp(self):
        self.driver = webdriver.Remote(desired_capabilities=capabilities,
                                       command_executor=config.get('seetest_urls', 'cloud_url') + config.get(
                                           'seetest_urls', 'wd_hub'))

    def test_wifi_connection(self):
        # Storing device Serial Number to variable
        device_udid = self.driver.capabilities['udid']

        # Getting Device ID from SeeTestCloud with an API call
        device_id = get_device_id(device_udid)

        # Storing WiFi Connection in text format
        wifi_label = self.driver.find_element(By.XPATH,
                                              "(//*[@id='Wi-Fi']//XCUIElementTypeStaticText)[2]").text  # XPATH applicable for iOS 12 / 13 / 14 / 15 - Checked both iPhone & iPad

        # Check if the desired WiFi name is present in the connected WiFi
        if config.get('wifi', 'wifi_name') in wifi_label:
            logger('Python Script - Connected to correct WiFi: %s' % wifi_label)
            # remove all device tags with an API call
            remove_all_device_tags(device_id)
            # add custom device tag with an API call
            add_device_tag(device_id, config.get('tags', 'good_tag_value'))
        else:
            logger('Python Script - Not Connected to correct WiFi: %s' % wifi_label)
            # remove all device tags with an API call
            remove_all_device_tags(device_id)
            # add custom device tag with an API call
            add_device_tag(device_id, config.get('tags', 'bad_tag_value'))

    def tearDown(self):
        # Marking the test as passed, otherwise cloud device will remain in 'Cleanup Failed' mode
        status = 'passed'
        # Ending the device reservation session
        self.driver.quit()
        # Marking the test as passed, and finishes up the cleanup session
        finish_cleanup_state(uid, status)


# Helps run the test using unittest framework
runner = unittest.TextTestRunner()
suite = unittest.TestLoader().loadTestsFromTestCase(SampleTestCase)
