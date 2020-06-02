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
        if arg:
            func(arg)
        else:
            func()
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

    WebDriverWait(driver, 45).until(
        EC.presence_of_element_located((By.LINK_TEXT, CREATE_TEXT)))
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
    submit_btn = driver.find_element_by_id(SUBMIT_BTN_ID)
    timeoutCatcher(driver, submit_btn.click)

def nav_quiz_edit_page(driver, scrape_data):
    """
    :param driver: selenium driver. Should currently be the page for entering the
                   details of the quiz
    :param scrape_data: named tuple of song data. Title, artist, lyrics

    Enters details for the quiz and submits brings to the test page.
    """

    #text prompts
    desc_prompt = f'Can you recite the lyrics of {scrape_data.title} by {scrape_data.artist}?'
    answer_type = "Lyric"

    #HTML constants for element id/class names
    DESC_NAME = "game_rightlingo"
    TIMER_NAME = "game_timer"
    ANSWER_TYPE_NAME = "game_enter_lingo"
    HINT_HEADING_NAME = "game_element_name"
    ANSWER_HEADING_NAME = "game_element_value"
    CATEGORY_NAME = "category"
    SAVE_BTN_NAME = "submitgame"
    DATA_TAB_ID = "elementstab"
    SOURCE_NAME = "sourceurl"

    #wait until elements are loaded
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, DESC_NAME)))

    timer_elem = driver.find_element_by_name(TIMER_NAME)
    category_elem = driver.find_element_by_name(CATEGORY_NAME)

    #fill out form input fields
    driver.find_element_by_name(DESC_NAME).send_keys(desc_prompt)

    input_answer_type = driver.find_element_by_name(ANSWER_TYPE_NAME)
    input_answer_type.clear()
    input_answer_type.send_keys(answer_type)

    driver.find_element_by_name(HINT_HEADING_NAME).clear()
    driver.find_element_by_name(ANSWER_HEADING_NAME).clear()
    driver.find_element_by_name(SOURCE_NAME).send_keys(scrape_data.sourceurl)

    #fillout form quiz timer select field
    actions = ActionChains(driver)

    actions.move_to_element(timer_elem)
    actions.click(timer_elem)
    actions.perform()

    driver.find_element_by_xpath("//select[@name='game_timer']/option[text() = '15:00']").click()

    #scroll down
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    #fillout form category select field
    actions.move_to_element(category_elem)
    actions.click(category_elem)
    actions.perform()

    driver.find_element_by_xpath("//select[@name='category']/option[text() = 'Music']").click()

    #save changes
    driver.find_element_by_name(SAVE_BTN_NAME).click()

    #open data tab
    data_btn = driver.find_element_by_id(DATA_TAB_ID)
    timeoutCatcher(driver, data_btn.click)

def nav_quiz_data_page(driver, scrape_data):
    """
    :param driver: selenium driver. Should currently be the page for entering the
                   details of the quiz
    :param scrape_data: named tuple of song data. Title, artist, lyrics

    Enters details for the quiz and submits brings to the test page.
    """

    #HTML constants for element id/class names
    IMPORT_DATA_TXT = "Import Data"
    IMPORT_C = "submit-btn"
    DATA_TXT_BOX_ID = "enter_box"

    #open data page
    driver.find_element_by_link_text(IMPORT_DATA_TXT).click()

    #wait for text box to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, DATA_TXT_BOX_ID)))

    #enter data into text box
    text_box = driver.find_element_by_id(DATA_TXT_BOX_ID)
    text_box.click()

    for word in scrape_data.lyrics:
        text_box.send_keys(word)
        text_box.send_keys(Keys.RETURN)

    #delete trailing return
    text_box.send_keys(Keys.BACKSPACE)

    #import
    driver.find_element_by_class_name(IMPORT_C).click()

def nav_to_end(driver):
    """
    :param driver: selenium driver. Should currently be the page for entering the
                   details of the quiz

    Final navigation to the "finish up" tab and making quiz private
    """

    FINISH_ID = "donetab"
    TOS_CHECK_BOX_ID = "accept-tos-checkbox"
    PRIVATE_QUIZ_ID = "launch_private_quiz"

    #navigate to finish up page and make quiz private before closing
    driver.find_element_by_id(FINISH_ID).click()
    driver.find_element_by_id(TOS_CHECK_BOX_ID).click()
    driver.find_element_by_id(PRIVATE_QUIZ_ID).click()


if __name__ == "__main__":
    Song = namedtuple("Song", "title artist lyrics sourceurl")
    SL = Song(title="Childhood's End", artist="Iron Maiden", lyrics=["hi", "my"], sourceurl = "https://www.lyrics.com/lyric/36440596/Childhood%E2%80%99s+End") #testing

    driver = setup_driver()

    nav_login_page(driver)
    nav_to_creation_page(driver)
    nav_creation_page(driver, SL)
    nav_quiz_edit_page(driver, SL)
    nav_quiz_data_page(driver, SL)
    nav_to_end(driver)
    driver.close()
