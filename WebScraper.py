import urllib.request
from collections import namedtuple
from bs4 import BeautifulSoup

def run(url):
    """
    :param url: url from Lyrics.com
    #TODO: validate URL
    #TODO: error handling:
       1. if page isn't found
       2. if page structure changes
    """
    #container to return song info
    Song = namedtuple("Song", "title artist lyrics sourceurl")

    soup = get_soup(url)
    title = get_title(soup)
    artist = get_artist(soup)
    lyrics = get_lyrics(soup)

    return Song(title=title, artist=artist, lyrics=lyrics, sourceurl=url)

def get_soup(url):
    """
    :param url: string object of url to Lyrics.com song lyric page

    Initialize and return beautiful soup object with URL
    """
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    return BeautifulSoup(response, 'html.parser')

def get_title(soup):
    """
    :param url: string object of url to Lyrics.com song lyric page

    Scrape website for song title and return it
    """
    return soup.find_all(id='lyric-title-text')[0].string

def get_artist(soup):
    """
    :param url: string object of url to Lyrics.com song lyric page

    Scrape website for song artist and return it
    """
    return soup.find_all('h3', 'lyric-artist')[0].contents[0].string

def get_lyrics(soup):
    """
    :param url: string object of url to Lyrics.com song lyric page

    Scrape website for song lyrics and return it
    """
    lyrics = []
    raw = soup.find_all(id='lyric-body-text')[0].contents
    for line in raw:
        """
        line below eliminates <a> tags in lyrics where
        the words are linked with definitions
        """
        line = line.string

        lyrics += line.split()

    return lyrics

#for testing purposes
#TODO: remove after class is complete
if __name__ == "__main__":
    url = "https://www.lyrics.com/lyric/36440596/Childhood%E2%80%99s+End"
    print(run(url))
