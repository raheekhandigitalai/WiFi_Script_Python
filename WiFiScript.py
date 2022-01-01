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

from APIs import remove_all_device_tags
from APIs import add_device_tag
from APIs import get_device_property
from APIs import finish_cleanup_state

from appium import webdriver
from selenium.webdriver import DesiredCapabilities

status = 'failed'

uid = os.getenv("deviceID")
operating_system = os.getenv("deviceOS")

# Pre-defining the iPhone capabilities as script is designed for iOS only for now
capabilities = DesiredCapabilities.IPHONE

# config.properties reader
config = configparser.ConfigParser()
config.read('config.properties')


class SampleTestCase(unittest.TestCase):
    # def test_2(self):
    #     print(get_device_os_version('56793ec400fe2121df8a6341591cbd25b7c26c70'))

    # Android currently not supported. If Device is Android, exit the script before it starts
    if operating_system == 'Android':
        logger('Python Script (logger) - operating_system is android, not yet supported: %s' % operating_system)
        # Marking the test as passed, otherwise cloud device will remain in 'Cleanup Failed' mode
        status = 'passed'
        # Marking the test as passed, and finishes up the cleanup session
        finish_cleanup_state(uid, status)
        # Exiting script
        sys.exit()

    # if iOS - Do nothing, continue test as usual
    elif operating_system == 'iOS':
        logger('Python Script (logger) - operating_system is ios, continuing: %s' % operating_system)

    # Capabilities for the session
    capabilities['testName'] = 'Webhook cleanup'
    capabilities['accessKey'] = '%s' % config.get('seetest_authorization', 'access_key_cleanup')
    # capabilities['accessKey'] = '%s' % config.get('seetest_authorization', 'access_key_admin')
    capabilities['udid'] = '%s' % uid
    # capabilities['udid'] = '00008020-000275D43CD8003A'
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
        device_id = get_device_property(device_udid, 'id')

        # Getting Device OS Version from SeeTestCloud with an API call
        device_os_version = get_device_property(device_udid, 'osVersion')

        # Getting Device Category (PHONE / TABLET) from SeeTestCloud with an API call
        device_category = get_device_property(device_udid, 'deviceCategory')

        # Wait for element to be present before interacting
        wait_for_element_to_be_present(self.driver, Locators.wifi_xpath)

        # Storing Wi-Fi Connection in text format
        wifi_label = get_text_from_element(self.driver, Locators.wifi_xpath)

        # Check if the desired Wi-Fi name is present in the connected Wi-Fi
        if config.get('wifi', 'wifi_name') in wifi_label:
            logger('Python Script (logger) - Connected to correct Wi-Fi: %s' % wifi_label)
            # remove all device tags with an API call
            remove_all_device_tags(device_id)
            # add custom device tag with an API call
            add_device_tag(device_id, config.get('tags', 'good_tag_value'))
        else:
            logger('Python Script (logger) - Not Connected to correct Wi-Fi: %s' % wifi_label)
            # remove all device tags with an API call
            remove_all_device_tags(device_id)
            # add custom device tag with an API call
            add_device_tag(device_id, config.get('tags', 'bad_tag_value'))

        # List to be populated by the profiles found
        # General > Profile (iOS 14 and below)
        # General > VPN & Device Management (iOS 15 +)
        profiles = []

        # Check if script is being triggered against iPad. If so, then I want to avoid additional steps like scrolls.
        # On smaller screen sizes "General" may not appear and scroll may be needed.
        if device_category == 'TABLET':
            # Wait for element and click
            wait_for_element_to_be_present_and_click(self.driver, Locators.general_xpath)

            # iOS 15 + does not have 'profiles' under 'General'. It is instead VPN and Device Management
            if '15' in device_os_version:
                # Wait for element and click on 'VPN & Device Management'
                wait_for_element_to_be_present_and_click(
                    self.driver, Locators.vpn_and_device_management_xpath)

                # Store profiles in a list
                profiles = find_elements(self.driver,
                                         Locators.profiles_list_xpath)

                # Iterate and list out each profile present
                logger('Python Script (logger) - Printing all available Profiles ==>')
                for profile in profiles:
                    logger('Python Script (logger) - profile: %s' % profile.text)
                    # Add logic on what to be done if profile found / not found
                logger('Python Script (logger) - <== End of printing all available Profiles')

            else:
                # Wait for element and click on 'Profile'
                wait_for_element_to_be_present_and_click(
                    self.driver, Locators.profile_xpath)

                # Store profiles in a list
                profiles = find_elements(self.driver,
                                         Locators.profiles_list_xpath)

                # Iterate and list out each profile present
                logger('Python Script (logger) - Printing all available Profiles ==>')
                for profile in profiles:
                    logger('Python Script (logger) - profile: %s' % profile.text)
                    # Add logic on what to be done if profile found / not found
                logger('Python Script (logger) - <== End of printing all available Profiles')

        elif device_category == 'PHONE':
            # Implement swipe
            # Implement click on General

            # iOS 15 + does not have 'profiles' under 'General'. It is instead VPN and Device Management
            if '15' in device_os_version:
                logger('')  # Implement click on 'VPN & Device Management' and Implement storing profiles into a list
            else:
                logger('')  # Implement click on 'Profile' and Implement storing profiles into a list

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
