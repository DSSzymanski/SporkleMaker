import config
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    SPORCLE_QUIZ = "https://www.sporcle.com"
    driver = webdriver.Firefox()
    driver.get(SPORCLE_QUIZ)
    return driver

def nav_login_page(driver):
    """
    :param driver: selenium driver already setup and set to Sporcle website

    Procedure navagates home sporcle page and logs in using the login javascript
    popup. Should end on home page and logged in.
    """
    #get login information from config class
    USER_EMAIL = config.get_username()
    USER_PASSWORD = config.get_password()

    #HTML constants for element id/class names
    LOGIN_BTN_ID = "user-not-logged-in"
    USERNAME_C_NAME = "textinput usernameInput"
    PASSWORD_C_NAME = "textinput passwordInput"
    SUBMIT_BTN_C_NAME = "buttonShape buttonGreen log-in-button"
    """
    WebDriverWait(driver, 200).until(EC.presence_of_element_located(By.ID, LOGIN_BTN_ID))
    #click login button
    driver.find_element_by_id(LOGIN_BTN_ID).click()
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(By.CLASS_NAME, SUBMIT_BTN_C_NAME))
    #enter login information
    driver.find_element_by_class_name(USERNAME_C_NAME).send_keys(USER_EMAIL)
    driver.find_element_by_class_name(PASSWORD_C_NAME).send_keys(USER_PASSWORD)
    #submit
    driver.find_element_by_class_name(SUBMIT_BTN_C_NAME).click()
    """
    return driver

"""
def nav_creation_page(scraper_list):

    TODO: access "game_name" input box and insert song title name
    TODO: access "quiz_type" select box and make sure option 0: "Classic" is selected
    TODO: access "submit" button and click

    song_name = scraper_list[0]
    driver.find_element_by_name("game_name").send_keys(song_name)
"""

if __name__ == "__main__":
    Song = namedtuple("Song", "title artist lyrics")
    SL = ["Childhood's End", "Iron Maiden", ["hi", "my"]] #testing
    driver = setup_driver()
    nav_login_page(driver)
    #nav_creation_page(SL)
    #driver.close()