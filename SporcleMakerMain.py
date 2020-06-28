import webScraper
import SporcleHandler

if __name__ == "__main__":
    print("Enter Lyrics.com url here:")
    url = input()
    song = webScraper.run(url)
    SporcleHandler.run(song)