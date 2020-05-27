import urllib.request
from bs4 import BeautifulSoup

class LyricGetter:
    def __init__(self, url):
        """
        :param url: url from Lyrics.com
        #TODO: validate URL
        #TODO: error handling:
           1. if page isn't found
           2. if page structure changes
        """
        self.url = url
        self.soup = self._get_soup()
        #container to store lyrics word by word
        self.lyrics = []
        #initializes info about song. Title, artist, lyrics
        self._init_title()
        self._init_artist()
        self._init_lyrics()

    def _get_soup(self):
        """Initialize beautiful soup object with URL"""
        req = urllib.request.Request(self.url)
        response = urllib.request.urlopen(req)
        return BeautifulSoup(response, 'html.parser')

    def _init_title(self):
        """Scrape website for song title and store in class var"""
        self.title = self.soup.find_all(id='lyric-title-text')[0].string

    def _init_artist(self):
        """Scrape website for song artist and store in class var"""
        self.artist = self.soup.find_all('h3', 'lyric-artist')[0].contents[0].string

    def _init_lyrics(self):
        """Scrape website for song lyrics and store in class container"""
        raw = self.soup.find_all(id='lyric-body-text')[0].contents
        for line in raw:
            """
            line below eliminates <a> tags in lyrics where
            the words are linked with definitions
            """
            line = line.string

            self.lyrics += line.split()

    def get_lyrics(self):
        """Return the lyrics of song in []"""
        return self.lyrics

    def get_artist(self):
        """Return the artist(str) of song"""
        return self.artist

    def get_title(self):
        """Return the title(str) of song"""
        return self.title

#for testing purposes
#TODO: remove after class is complete
if __name__ == "__main__":
    url = "https://www.lyrics.com/lyric/36440596/Childhood%E2%80%99s+End"
    LG = LyricGetter(url)
