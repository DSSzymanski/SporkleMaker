import config
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def nav_login_page():
    USER_EMAIL = config.get_username()
    USER_PASSWORD = config.get_password()

def nav_creation_page(scraper_list):
    """
    TODO: access "game_name" input box and insert song title name
    TODO: access "quiz_type" select box and make sure option 0: "Classic" is selected
    TODO: access "submit" button and click
    """
    SPORCLE_QUIZ_URL = "https://www.sporcle.com/create/new"

    driver = webdriver.Firefox()
    driver.get(SPORCLE_QUIZ_URL)
    assert "Python" in driver.title

    song_name = scraper_list[0]
    driver.find_element_by_name("game_name").send_keys(song_name)
    driver.close()

if __name__ == "__main__":
    Song = namedtuple("Song", "title artist lyrics")
    SL = ["Childhood's End", "Iron Maiden", ["hi", "my"]]
    nav_creation_page(SL)