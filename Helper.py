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


def wait_for_element_to_be_present_and_click(driver, xpath):
    wait_for_element_to_be_present(driver, xpath)
    driver.find_element(By.XPATH, xpath).click()


def find_elements(driver, xpath):
    items = driver.find_elements(By.XPATH, xpath)
    return items


def get_text_from_element(driver, xpath):
    value = driver.find_element(By.XPATH, xpath).text
    return value
