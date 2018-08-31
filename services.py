"""Service functions for formatting scraped HTML
"""

import http_requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_word_definitions(word: str) -> list:
    """ A facilitating function to call and ingest the incoming blob 
    from the UD rest call, parse out the definitions by html 
    tag, format the definintions & append them to a list to be
    returned
    
    Arguments:
        word {str} -- word to be defined
    
    Returns:
        definitions {list} -- a formatted list of definitions 
    """
    definition_blob = http_requests.get_word_definition(word)
    soup = BeautifulSoup(definition_blob, "html.parser")
    definitions = []
    raw_definitions = soup.find_all(class_="def-panel")
    for raw_definition in raw_definitions:
        definitions.append(_format_single_definition(str(raw_definition)))
    return definitions


def _format_single_definition(raw_definition: str) -> dict:
    """Takes a single definition in HTML format and parses out the parts
    we care about using HTML class tags
    
    Arguments:
        raw_definition {str} -- HTML formatted version of the definition
    
    Returns:
        definition {dict} -- dict formatted version of the definition
    """
    soup = BeautifulSoup(raw_definition, "html.parser")

    raw_meaning = soup.find_all(class_="meaning")
    meaning = _format_raw_html(raw_meaning)
    logger.info("Meaning: {}\n".format(meaning))

    raw_example = soup.find_all(class_="example")
    example = _format_raw_html(raw_example)
    logger.info("Example: {}\n".format(example))

    raw_contributor = soup.find_all(class_="contributor")
    contributor = _format_raw_html(raw_contributor)
    logger.info("Contributer: {}\n".format(contributor))

    definition = {
        'meaning': meaning,
        'example': example,
        'contributor': contributor
    }
    return definition


def _format_raw_html(raw_html: str) -> str:
    """ Facilitating function to remove various HTML formatting tags 
    and symbols for easier parsing
    
    Arguments:
        raw_html {str} -- HTML string to be pruned
    
    Returns:
        formatted {str} -- raw content stripped of HTML
    """
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
    """Function to remove a particular HTML tag from a string while
    preserveing the raw data inside the tag itself
    
    Arguments:
        raw_html {str} -- string to manipulate
        remove_tag {str} -- tag to be removed
    
    Returns:
        soup {str} -- string without the removed tag
    """
    soup = BeautifulSoup(str(raw_html), "html.parser")
    tags = soup.select(remove_tag)
    for tag in tags:
        temp_string = tag.string
        tag.replace_with(temp_string)
    return soup


def _remove_replace_outer_div(raw_html: str) -> str:
    """Remove the outer divs of a string... DO I NEED?
    
    Arguments:
        raw_html {str} -- string to manipulate
    
    Returns:
        temp_string {str} -- div free string
    """
    soup = BeautifulSoup(str(raw_html), "html.parser")
    div = soup.select("div")
    for div in div:
        temp_string = div.string
    return temp_string


def _remove_tag(raw_html: str, remove_tag: str) -> str:
    """Remove all instances of a single tag without need replace
    
    Arguments:
        raw_html {str} -- string to manipulate
        remove_tag {str} -- tag to remove
    
    Returns:
        soup {str} -- [description]
    """
    soup = BeautifulSoup(str(raw_html), "html.parser")
    tags = soup.select(remove_tag)
    for tag in tags:
        tag.decompose()
    return soup