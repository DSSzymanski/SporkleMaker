import config
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#for timeout of main page load
from selenium.common.exceptions import TimeoutException

def timeoutCatcher(driver, func, arg=None):
    """
    :param driver: selenium driver
    :param func: function to be ran that loads new web page
    :param arg: argument to be passed into function

    Ends long running scripts that don't effect web page when page is loaded
    """
    try:
        if arg: func(arg)
        else: func()
    except TimeoutException:
        driver.execute_script("window.stop();")

def setup_driver():
    """
    Sets up driver and loads sporcle in a firefox page
    """
    SPORCLE_QUIZ = "https://www.sporcle.com"
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(30)

    #get base sporcle page
    timeoutCatcher(driver, driver.get, SPORCLE_QUIZ)

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
    TODO: driver page seems to NOT load login button (and a few others) if a
    sporcle page is open in mozilla in another window
    """

    #click login button to open new frame to login
    driver.find_element_by_id(LOGIN_BTN_ID).click()

    #wait until login frame has loaded
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, USERNAME_C_NAME)))

    #enter login information and submit login
    driver.find_element_by_class_name(USERNAME_C_NAME).send_keys(USER_EMAIL)
    driver.find_element_by_class_name(PASSWORD_C_NAME).send_keys(USER_PASSWORD)
    submit = driver.find_element_by_class_name(SUBMIT_BTN_C_NAME)

    #submits and loads new page
    timeoutCatcher(driver=driver, func=submit.click)

def nav_to_creation_page(driver):
    """
    :param driver: selenium driver. Should be on sporcle home page already
        logged in

    Finds "CREATE" in header, hovers over it, then selects the create a quiz
    link to navigate to quiz creation page
    """
    #HTML constants for element id/class names
    CREATE_TEXT = "CREATE"
    NEW_QUIZ_TEXT = "CREATE A QUIZ"

    WebDriverWait(driver, 45)
    #store element to hover over to get the "create a quiz" link
    hover_elem = driver.find_element_by_link_text(CREATE_TEXT)

    #execute hover
    actions = ActionChains(driver)
    actions.move_to_element(hover_elem)
    actions.perform()

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.LINK_TEXT, NEW_QUIZ_TEXT)))
    #store new quiz element and click
    new_quiz_elem = driver.find_element_by_link_text(NEW_QUIZ_TEXT)
    actions.click(new_quiz_elem)
    actions.perform()

def nav_creation_page(driver, scrape_data):
    """
    :param driver: selenium driver. Should currently be the quiz creating page
    :param scrape_data: named tuple of song data. Title, artist, lyrics

    Navigates the sporcle page for creating the quiz
    """
    #Quiz name
    prompt = f'{scrape_data.title} lyrics by {scrape_data.artist}?'

    #HTML constants for element id/class names
    NAME_ID = "game_name"
    SUBMIT_BTN_ID = "submit"

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, NAME_ID)))
    #sends prompt to quiz name field
    driver.find_element_by_id(NAME_ID).send_keys(prompt)

    #submit
    driver.find_element_by_id(SUBMIT_BTN_ID).click()

#def nav_quiz_detail_page(driver, scrape_data):

if __name__ == "__main__":
    Song = namedtuple("Song", "title artist lyrics")
    SL = Song(title="Childhood's End", artist="Iron Maiden", lyrics=["hi", "my"]) #testing

    driver = setup_driver()

    nav_login_page(driver)
    nav_to_creation_page(driver)
    nav_creation_page(driver, SL)
    #driver.close()