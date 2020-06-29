import web_scraper
import sporcle_handler
import validator

if __name__ == "__main__":
    while True:
        print("Enter Lyrics.com url here:")
        url = input()
        valid = validator.validate_url(url)
        if valid:
            break

    song = web_scraper.run(url)
    sporcle_handler.run(song)