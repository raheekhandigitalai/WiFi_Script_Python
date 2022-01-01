# XPATHs stored under this file for re-usability and clean code in WiFiScript.py

wifi_xpath = "(//*[@id='Wi-Fi']//XCUIElementTypeStaticText)[2]"
general_xpath = "//XCUIElementTypeCell[@text='General']"
profile_xpath = "//XCUIElementTypeCell[contains(text(), 'Profile')]"
vpn_and_device_management_xpath = "//XCUIElementTypeCell[contains(text(), 'Device Management')]"
profiles_list_xpath = "//XCUIElementTypeOther[@text='CONFIGURATION PROFILE']/following-sibling::XCUIElementTypeCell"
