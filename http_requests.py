"""HTTP requests to urban dictionary
"""

import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URBAN_URL = "https://www.urbandictionary.com/"


def get_word_definition(word: str) -> object:
    """Request to urban dictionary site retrieving the html content the entire page of the word searched
    
    Arguments:
        word {str} -- word to define
    
    Returns:
        {object} -- the html content of the retrieved page
    """
    URL = URBAN_URL + "define.php"
    PARAMS = {'term': word}
    r = requests.get(url=URL, params=PARAMS)
    return r.text