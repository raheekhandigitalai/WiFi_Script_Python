import os
import unittest
import configparser
import sys

import Locators

from Helper import logger
from Helper import get_text_from_element
from Helper import find_elements
from Helper import wait_for_element_to_be_present
from Helper import wait_for_element_to_be_present_and_click

from appium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Pre-defining the iPhone capabilities as script is designed for iOS only for now
capabilities = DesiredCapabilities.IPHONE

# config.properties reader
config = configparser.ConfigParser()
config.read('config.properties')


def click_element_else_swipe_and_click(driver, xpath, start_offset):
    try:
        if driver.find_element(By.XPATH, xpath).is_displayed():
            driver.find_element(By.XPATH, xpath).click()
    except:
        driver.execute_script(
            "seetest:client.swipeWhileNotFound(\"DOWN\"," + str(start_offset) + ", 1000, \"NATIVE\", \"xpath=" + xpath + "\", 0, 1500, 2, true)")


class TestRunner(unittest.TestCase):

    capabilities['testName'] = 'Webhook cleanup'
    capabilities['accessKey'] = '%s' % config.get('seetest_authorization', 'access_key_admin')
    capabilities['udid'] = '00008020-001C2D201A90003A'
    capabilities['platformName'] = 'iOS'
    capabilities['autoDismissAlerts'] = True
    capabilities['releaseDevice'] = False
    capabilities['bundleId'] = 'com.apple.Preferences'
    capabilities['dontGoHomeOnQuit'] = True

    def setUp(self):
        self.driver = webdriver.Remote(desired_capabilities=capabilities,
                                       command_executor=config.get('seetest_urls', 'cloud_url') + config.get(
                                           'seetest_urls', 'wd_hub'))

    def test_wifi_connection(self):
        os_version = '15'

        if '15' in os_version:
            print('iOS 15')
            wait_for_element_to_be_present(self.driver, "//XCUIElementTypeNavigationBar[contains(text(), 'Settings')]")
            click_element_else_swipe_and_click(self.driver, "//XCUIElementTypeCell[@text='General' and @onScreen='true']", 1000)
            wait_for_element_to_be_present(self.driver, "//XCUIElementTypeCell[contains(text(), 'About')]")
            click_element_else_swipe_and_click(self.driver, "//XCUIElementTypeCell[contains(text(), 'Device Management') and @onScreen='true']", 400)

            profiles = find_elements(self.driver,
                                     Locators.profiles_list_xpath)

            # Iterate and list out each profile present
            logger('Python Script (logger) - Printing all available Profiles ==>')
            for profile in profiles:
                logger('Python Script (logger) - profile: %s' % profile.text)
                # Add logic on what to be done if profile found / not found
            logger('Python Script (logger) - <== End of printing all available Profiles')
        else:
            print('NOT iOS 15')
            wait_for_element_to_be_present(self.driver, "//XCUIElementTypeNavigationBar[contains(text(), 'Settings')]")
            click_element_else_swipe_and_click(self.driver, "//XCUIElementTypeCell[@text='General' and @onScreen='true']", 1000)
            wait_for_element_to_be_present(self.driver, "//XCUIElementTypeCell[contains(text(), 'About')]")
            click_element_else_swipe_and_click(self.driver, "//XCUIElementTypeCell[contains(text(), 'Profile') and @onScreen='true']", 400)

            profiles = find_elements(self.driver,
                                     Locators.profiles_list_xpath)

            # Iterate and list out each profile present
            logger('Python Script (logger) - Printing all available Profiles ==>')
            for profile in profiles:
                logger('Python Script (logger) - profile: %s' % profile.text)
                # Add logic on what to be done if profile found / not found
            logger('Python Script (logger) - <== End of printing all available Profiles')

    def tearDown(self):
        self.driver.quit()


runner = unittest.TextTestRunner()
suite = unittest.TestLoader().loadTestsFromTestCase(TestRunner)
