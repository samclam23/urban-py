import http_requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_word_definitions(word: str) -> dict:
    definition_blob = http_requests.get_word_definition(word)
    soup = BeautifulSoup(definition_blob, "html.parser")
    definitions = {}
    counter = 0
    raw_definitions = soup.find_all(class_="def-panel")
    for raw_definition in raw_definitions:
        definitions[counter] = _format_single_definition(str(raw_definition))   #TODO: get the dict in order
        counter+=1
    return definitions


def _format_single_definition(raw_definition: str) -> dict:
    soup = BeautifulSoup(raw_definition, "html.parser")

    raw_meaning = soup.find_all(class_="meaning")
   # logger.info("\n\n\n\n\n\n raw_meaning: {}".format(raw_meaning))
    meaning =  _format_raw_html(raw_meaning)

    raw_example = soup.find_all(class_="example")
   # logger.info("\n\n\n\n\n\n\n raw_example: {}".format(raw_example))
    example =  _format_raw_html(raw_example)

    raw_contributor = soup.find_all(class_="contributor")
   # logger.info("\n\n\n\n\n\n\n raw_contributor: {}".format(raw_contributor))
    contributor =  _format_raw_html(raw_contributor)

    definition = {
        'meaning': meaning,
        'example': example,
        'contributor': contributor
    }
    return definition


def _format_raw_html(raw_html: str) -> str:
    logger.info("\n Soup: {}".format(raw_html))   
    links_removed = _remove_links(raw_html)
    logger.info("After removing links: {}".format(links_removed))

    formatted = _remove_div(links_removed)
    logger.info("After formatting: {}".format(formatted))
    return formatted

def _remove_links(raw_html: str) -> str:
    soup = BeautifulSoup(str(raw_html), "html.parser")
    a_tags = soup.select("a")
    for a_tag in a_tags:
        temp_string = a_tag.string
        a_tag.replace_with(temp_string)
    return soup


def _remove_div(raw_html: str) -> str:
    soup = BeautifulSoup(str(raw_html), "html.parser")
    div = soup.select("div")
    for div in div:
        temp_string = div.string
    return temp_string




