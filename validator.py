"""
Validator module to validate inputs.
"""

#URL ERRORS
#prints error if url is too small to possibly be a Lyrics.com URL
URL_SIZE_E = "The link you have entered is too small to be a valid \
Lyrics.com url.\n"

#prints error if url is not lyrics.com
URL_LINK_ERROR = "The link you entered needs to be from Lyrics.com starting \
with lyrics.com/ or http://lyrics.com/.\n"
#END URL ERRORS

def validate_url(url):
    """
    Validates that url belongs to the website lyrics.com. Will not detect if
    link is a valid song title page.

    :param url: url entered through command prompt
    """
    standard = "www.lyrics.com/"
    standard_len = len(standard)
    extended = "https://www.lyrics.com/"
    extended_len = len(extended)

    if isinstance(url, str):
        if len(url) < standard_len-1:
            print(URL_SIZE_E)
            return False
        if url[:standard_len] == standard:
            return True
        elif url[:extended_len] == extended:
            return True
        print(URL_LINK_ERROR)
    return False
