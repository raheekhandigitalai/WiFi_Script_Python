# XPATHs stored under this file for re-usability and clean code in WiFiScript.py

settings_navigation_bar_xpath = "//XCUIElementTypeNavigationBar[contains(text(), 'Settings')]"
wifi_xpath = "(//*[@id='Wi-Fi']//XCUIElementTypeStaticText)[2]"
general_xpath = "//XCUIElementTypeCell[@text='General']"
general_with_onscreen_xpath = "//XCUIElementTypeCell[@text='General' and @onScreen='true']"
about_xpath = "//XCUIElementTypeCell[contains(text(), 'About')]"
profile_xpath = "//XCUIElementTypeCell[contains(text(), 'Profile')]"
profile_with_onscreen_property_xpath = "//XCUIElementTypeCell[contains(text(), 'Profile') and @onScreen='true']"
vpn_and_device_management_xpath = "//XCUIElementTypeCell[contains(text(), 'Device Management')]"
vpn_and_device_management_with_onscreen_property_xpath = "//XCUIElementTypeCell[contains(text(), 'Device Management') and @onScreen='true']"
profiles_list_xpath = "//XCUIElementTypeOther[@text='CONFIGURATION PROFILE']/following-sibling::XCUIElementTypeCell"
