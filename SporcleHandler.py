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
    frame. Should end on home page and logged in.
    """
    #get login information from config class
    USER_EMAIL = config.get_username()
    USER_PASSWORD = config.get_password()

    #HTML constants for element id/class names
    LOGIN_BTN_ID = "user-not-logged-in"
    USERNAME_C_NAME = "usernameInput"
    PASSWORD_C_NAME = "passwordInput"
    SUBMIT_BTN_C_NAME = "log-in-button"

    """
    wait for page to fully load. Login button seems to not load unil last
    200 second wait because firefox page first load seems to take forever on
    shitty wifi
    """
    """
    TODO: driver page seems to NOT load login button (and a few others) if a
    sporcle page is open in mozilla in another window
    """
    WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.ID, LOGIN_BTN_ID)))

    #click login button to open new frame to login
    driver.find_element_by_id(LOGIN_BTN_ID).click()

    #wait until login frame has loaded
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, USERNAME_C_NAME)))

    #enter login information and submit login
    driver.find_element_by_class_name(USERNAME_C_NAME).send_keys(USER_EMAIL)
    driver.find_element_by_class_name(PASSWORD_C_NAME).send_keys(USER_PASSWORD)
    driver.find_element_by_class_name(SUBMIT_BTN_C_NAME).click()

def nav_creation_page(scraper_list):
    """
    TODO: access "game_name" input box and insert song title name
    TODO: access "quiz_type" select box and make sure option 0: "Classic" is selected
    TODO: access "submit" button and click
    """
    song_name = scraper_list[0]
    driver.find_element_by_name("game_name").send_keys(song_name)

if __name__ == "__main__":
    Song = namedtuple("Song", "title artist lyrics")
    SL = ["Childhood's End", "Iron Maiden", ["hi", "my"]] #testing
    driver = setup_driver()
    nav_login_page(driver)
    #nav_creation_page(SL)
    #driver.close()