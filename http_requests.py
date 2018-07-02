import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URBAN_URL = "https://www.urbandictionary.com/"

def get_word_definition( word: str ):
    URL = URBAN_URL + "define.php"
    PARAMS = {'term': word}
    r = requests.get(url = URL, params = PARAMS)
    return r.text