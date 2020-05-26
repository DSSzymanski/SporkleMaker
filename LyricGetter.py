# -*- coding: utf-8 -*-
"""
Spyder Editor
"""
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

class LyricGetter:
	def __init__(self, url):
		self.url = url
		self.soup = self._get_soup()
		self.lyrics = []
		self._init_title()
		self._init_artist()
		self._init_lyrics()
		
	def _get_soup(self):
		req = urllib.request.Request(self.url)
		response = urllib.request.urlopen(req)
		return BeautifulSoup(response, 'html.parser')
	
	def _init_title(self):
		self.title = self.soup.find_all(id='lyric-title-text')[0].string
	
	def _init_artist(self):
		self.artist = self.soup.find_all('h3','lyric-artist')[0].contents[0].string
	
	def _init_lyrics(self):
		raw = self.soup.find_all(id='lyric-body-text')[0].contents
		for line in raw:
			line = line.string
			self.lyrics += line.split()
			
	def get_lyrics(self): return self.lyrics
		
		
if __name__ == "__main__":
	url = "https://www.lyrics.com/lyric/36440596/Childhood%E2%80%99s+End"
	LG = LyricGetter(url)
	LG.lyrics_to_csv()
