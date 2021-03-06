from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Re-usable method for logging purposes
def logger(content):
    print(content)


# Re-usable method for waiting on element to be present
def wait_for_element_to_be_present(driver, xpath):
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, xpath)))


# Re-usable method for waiting on element to be present and then click
def wait_for_element_to_be_present_and_click(driver, xpath):
    driver.wait_for_element_to_be_present(driver, xpath)
    driver.find_element(By.XPATH, xpath).click()


# Re-usable method to get text from element
def get_text_from_element(driver, xpath):
    value = driver.find_element(By.XPATH, xpath).text
    return value


# Re-usable method for getting elements in a list format
def find_elements(driver, xpath):
    items = driver.find_elements(By.XPATH, xpath)
    return items


# Re-usable method to click on element if found, else swipe and click
def click_element_else_swipe_and_click(driver, xpath, start_offset):
    try:
        if driver.find_element(By.XPATH, xpath).is_displayed():
            driver.find_element(By.XPATH, xpath).click()
    except:
        driver.execute_script("seetest:client.swipeWhileNotFound(\"DOWN\"," + str(start_offset) +
                              ", 1000, \"NATIVE\", \"xpath=" + xpath + "\", 0, 1500, 2, true)")

