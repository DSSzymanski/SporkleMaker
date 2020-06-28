"""
This module is used to navigate through the sporcle website. Page will log in
given the credentials listed in config.py and navigate the quiz creation page
and create a quiz given the song information in song input.

Run program will end and close out of the driver connection. It will initially
create the quiz as private so that you can manually check that the quiz data
was inputed correctly if desired before making the quiz public.

Example:
    sporcle_handler.run(song)
"""
#selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#for timeout of main page load
from selenium.common.exceptions import TimeoutException

import config

def run(song):
    """
    :param scrape_data: named tuple of song data. Title, artist, lyrics, sourceurl

    Main algorithm for the program
    """
    driver = setup_driver()
    #navigate pages
    nav_login_page(driver)
    nav_to_creation_page(driver)
    nav_creation_page(driver, song)
    nav_quiz_edit_page(driver, song)
    nav_quiz_data_page(driver, song)
    nav_to_end(driver)
    #close
    driver.close()

def timeout_catcher(driver, func, arg=None):
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
    sporcle_quiz = "https://www.sporcle.com"
    driver = webdriver.Firefox()
    driver.set_page_load_timeout(30)

    #get base sporcle page
    timeout_catcher(driver, driver.get, sporcle_quiz)

    return driver

def nav_login_page(driver):
    """
    :param driver: selenium driver already setup and set to Sporcle website

    Procedure navagates home sporcle page and logs in using the login javascript
    frame. Should end on home page and logged in.
    """
    #get login information from config class
    user_email = config.get_username()
    user_password = config.get_password()

    #HTML constants for element id/class names
    login_btn_id = "user-not-logged-in"
    username_c_name = "usernameInput"
    password_c_name = "passwordInput"
    submit_btn_c_name = "log-in-button"

    #click login button to open new frame to login
    driver.find_element_by_id(login_btn_id).click()

    #wait until login frame has loaded
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, username_c_name)))

    #enter login information and submit login
    driver.find_element_by_class_name(username_c_name).send_keys(user_email)
    driver.find_element_by_class_name(password_c_name).send_keys(user_password)
    submit = driver.find_element_by_class_name(submit_btn_c_name)

    #submits and loads new page
    timeout_catcher(driver=driver, func=submit.click)

def nav_to_creation_page(driver):
    """
    :param driver: selenium driver. Should be on sporcle home page already
        logged in

    Finds "CREATE" in header, hovers over it, then selects the create a quiz
    link to navigate to quiz creation page
    """
    #HTML constants for element id/class names
    create_text = "CREATE"
    new_quiz_text = "CREATE A QUIZ"

    WebDriverWait(driver, 45).until(
        EC.presence_of_element_located((By.LINK_TEXT, create_text)))
    #store element to hover over to get the "create a quiz" link
    hover_elem = driver.find_element_by_link_text(create_text)

    #execute hover
    actions = ActionChains(driver)
    actions.move_to_element(hover_elem)
    actions.perform()

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.LINK_TEXT, new_quiz_text)))
    #store new quiz element and click
    new_quiz_elem = driver.find_element_by_link_text(new_quiz_text)
    actions.click(new_quiz_elem)
    actions.perform()

def nav_creation_page(driver, scrape_data):
    """
    :param driver: selenium driver. Should currently be the quiz creating page
    :param scrape_data: named tuple of song data. Title, artist, lyrics, sourceurl

    Navigates the sporcle page for creating the quiz
    """
    #Quiz name
    prompt = f'{scrape_data.title} lyrics by {scrape_data.artist}?'

    #HTML constants for element id/class names
    name_id = "game_name"
    submit_btn_id = "submit"

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, name_id)))
    #sends prompt to quiz name field
    driver.find_element_by_id(name_id).send_keys(prompt)

    #submit
    submit_btn = driver.find_element_by_id(submit_btn_id)
    timeout_catcher(driver, submit_btn.click)

def nav_quiz_edit_page(driver, scrape_data):
    """
    :param driver: selenium driver. Should currently be the page for entering the
                   details of the quiz
    :param scrape_data: named tuple of song data. Title, artist, lyrics, sourceurl

    Enters details for the quiz and submits brings to the test page.
    """

    #text prompts
    desc_prompt = f'Can you recite the lyrics of {scrape_data.title} by {scrape_data.artist}?'
    answer_type = "Lyric"

    #HTML constants for element id/class names
    desc_name = "game_rightlingo"
    timer_name = "game_timer"
    answer_type_name = "game_enter_lingo"
    hint_heading_name = "game_element_name"
    answer_heading_name = "game_element_value"
    category_name = "category"
    save_btn_name = "submitgame"
    data_tab_id = "elementstab"
    source_name = "sourceurl"

    #wait until elements are loaded
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, desc_name)))

    timer_elem = driver.find_element_by_name(timer_name)
    category_elem = driver.find_element_by_name(category_name)

    #fill out form input fields
    driver.find_element_by_name(desc_name).send_keys(desc_prompt)

    input_answer_type = driver.find_element_by_name(answer_type_name)
    input_answer_type.clear()
    input_answer_type.send_keys(answer_type)

    driver.find_element_by_name(hint_heading_name).clear()
    driver.find_element_by_name(answer_heading_name).clear()
    driver.find_element_by_name(source_name).send_keys(scrape_data.sourceurl)

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
    driver.find_element_by_name(save_btn_name).click()

    #open data tab
    data_btn = driver.find_element_by_id(data_tab_id)
    timeout_catcher(driver, data_btn.click)

def nav_quiz_data_page(driver, scrape_data):
    """
    :param driver: selenium driver. Should currently be the page for entering the
                   details of the quiz
    :param scrape_data: named tuple of song data. Title, artist, lyrics, sourceurl

    Enters details for the quiz and submits brings to the test page.
    """

    #HTML constants for element id/class names
    import_data_txt = "Import Data"
    import_c = "submit-btn"
    data_txt_box_id = "enter_box"

    #open data page
    driver.find_element_by_link_text(import_data_txt).click()

    #wait for text box to load
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, data_txt_box_id)))

    #enter data into text box
    text_box = driver.find_element_by_id(data_txt_box_id)
    text_box.click()

    for word in scrape_data.lyrics:
        text_box.send_keys(word)
        text_box.send_keys(Keys.RETURN)

    #delete trailing return
    text_box.send_keys(Keys.BACKSPACE)

    #import
    driver.find_element_by_class_name(import_c).click()

def nav_to_end(driver):
    """
    :param driver: selenium driver. Should currently be the page for entering the
                   details of the quiz

    Final navigation to the "finish up" tab and making quiz private
    """

    finish_id = "donetab"
    tos_check_box_id = "accept-tos-checkbox"
    private_quiz_id = "launch_private_quiz"

    #navigate to finish up page and make quiz private before closing
    driver.find_element_by_id(finish_id).click()
    driver.find_element_by_id(tos_check_box_id).click()
    driver.find_element_by_id(private_quiz_id).click()
