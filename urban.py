import logging
import services

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_definitions( word: str ) -> list:
    definitions = services.get_word_definitions(word)
    for definition in definitions:
        logger.info("\n Definition: {}\n".format(definition))
    return definitions

def get_definition( word: str ) -> dict:
    definitions = services.get_word_definitions(word)
    logger.info("\n Definition: {}\n".format(definitions[0]))
    return definitions[0] 

get_definitions("hey")
get_definition("cool")