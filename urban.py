"""Main functions for calling urban dictionary definitions
"""

import logging
import services

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_definitions(word: str) -> list:
    """Get a page of definitions for one word from urban dictionary
    
    Arguments:
        word {str} -- The word to be defined
    
    Returns:
        list -- A list of parsed, reformatted definitions
    """
    definitions = services.get_word_definitions(word)
    for definition in definitions:
        logger.info("\n Definition: {}\n".format(definition))
    return definitions


def get_definition(word: str) -> dict:
    """Get the top definition for a passed word
    
    Arguments:
        word {str} -- The word to be defined
    
    Returns:
        dict -- A dict containing the top definition for the passed word
    """
    definitions = services.get_word_definitions(word)
    logger.info("\n Definition: {}\n".format(definitions[0]))
    return definitions[0] 


get_definitions("hey")
get_definition("cool")