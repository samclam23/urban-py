import logging
import services

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_definitions( word: str ) -> dict:
    definitions = services.get_word_definitions(word)
    logger.info("\n Definitions: {}\n".format(definitions))
    return None

get_definitions("cool")    