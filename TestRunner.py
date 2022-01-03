import unittest
import configparser

from appium import webdriver
from selenium.webdriver import DesiredCapabilities

# Pre-defining the iPhone capabilities as script is designed for iOS only for now
capabilities = DesiredCapabilities.IPHONE

# config.properties reader
config = configparser.ConfigParser()
config.read('config.properties')


# Using this class to test out logic before implementing in WiFiScript.py
class TestRunner(unittest.TestCase):

    capabilities['testName'] = 'Webhook cleanup test'
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
        print('')

    def tearDown(self):
        self.driver.quit()


runner = unittest.TextTestRunner()
suite = unittest.TestLoader().loadTestsFromTestCase(TestRunner)
