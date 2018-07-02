import http_requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_word_definitions(word: str) -> list:
    definition_blob = http_requests.get_word_definition(word)
    soup = BeautifulSoup(definition_blob, "html.parser")
    definitions = []
    raw_definitions = soup.find_all(class_="def-panel")
    for raw_definition in raw_definitions:
        definitions.append(_format_single_definition(str(raw_definition)))
    return definitions


def _format_single_definition(raw_definition: str) -> dict:
    soup = BeautifulSoup(raw_definition, "html.parser")

    raw_meaning = soup.find_all(class_="meaning")
    meaning =  _format_raw_html(raw_meaning)
    logger.info("Meaning: {}\n".format(meaning))

    raw_example = soup.find_all(class_="example")
    example =  _format_raw_html(raw_example)
    logger.info("Example: {}\n".format(example))

    raw_contributor = soup.find_all(class_="contributor")
    contributor =  _format_raw_html(raw_contributor)
    logger.info("Contributer: {}\n".format(contributor))

    definition = {
        'meaning': meaning,
        'example': example,
        'contributor': contributor
    }
    return definition


def _format_raw_html(raw_html: str) -> str:
    logger.info("\n Soup: {}\n".format(raw_html))
    br_removed = _remove_tag(raw_html, "br")

    bold_removed = _remove_replace_tag(br_removed, "b")
    italics_removed = _remove_replace_tag(bold_removed, "i")
    links_removed = _remove_replace_tag(italics_removed, "a")
    div_removed = _remove_replace_outer_div(links_removed)

    formatted = str(div_removed).replace('&apos;', '\'')
    logger.info("\n Formatted Soup: {}\n".format(formatted))
    return formatted


def _remove_replace_tag(raw_html: str, remove_tag: str) -> str:
    soup = BeautifulSoup(str(raw_html), "html.parser")
    tags = soup.select(remove_tag)
    for tag in tags:
        temp_string = tag.string
        tag.replace_with(temp_string)
    return soup


def _remove_replace_outer_div(raw_html: str) -> str:
    soup = BeautifulSoup(str(raw_html), "html.parser")
    div = soup.select("div")
    for div in div:
        temp_string = div.string
    return temp_string


def _remove_tag(raw_html: str, remove_tag: str) -> str:
    soup = BeautifulSoup(str(raw_html), "html.parser")
    tags = soup.select(remove_tag)
    for tag in tags:
        tag.decompose()
    return soup    




