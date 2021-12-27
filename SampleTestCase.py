import unittest
from APIs import remove_all_device_tags
from APIs import add_device_tag
from APIs import get_device_id
from appium import webdriver
from selenium.webdriver.common.by import By

desired_caps = dict(
    testName="PythonTest",
    accessKey="eyJ4cC51Ijo3MzU0MjQsInhwLnAiOjIsInhwLm0iOiJNVFUzT0RZd016ZzFOek16TVEiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE4OTM5NjM4NTcsImlzcyI6ImNvbS5leHBlcml0ZXN0In0.GP0hK0o0j2WEKt-J0aXsVbu1tmt-PhWUryqluokszJk",
    deviceQuery="@serialnumber='56793ec400fe2121df8a6341591cbd25b7c26c70'",
    platformName="iOS",
    bundleId="com.apple.Preferences"
)

wifi_name = "ECustomers_ALL_Legacy"
bad_tag_value = 'BadWiFi'
good_tag_value = 'GoodWiFi'


class SampleTestCase(unittest.TestCase):

    # def test_2(self):
    #     print(get_device_id('56793ec400fe2121df8a6341591cbd25b7c26c70'))

    def setUp(self):
        self.driver = webdriver.Remote('https://uscloud.experitest.com/wd/hub', desired_caps)

    def test_1(self):
        device_udid = self.driver.caps['udid']
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



    def tearDown(self):
        self.driver.quit()


runner = unittest.TextTestRunner()
suite = unittest.TestLoader().loadTestsFromTestCase(SampleTestCase)
