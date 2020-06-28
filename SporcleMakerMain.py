import web_scraper
import sporcle_handler

if __name__ == "__main__":
    print("Enter Lyrics.com url here:")
    url = input()
    song = web_scraper.run(url)
    sporcle_handler.run(song)