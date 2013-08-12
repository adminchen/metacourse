import logging
from lxml import html
from lxml.cssselect import CSSSelector
import re


LANGUAGES_LIST_URL = 'http://www.ted.com/translate/languages'
_LANGUAGES_SELECTOR = CSSSelector('div#content div div ul li a')
_LANGUAGE_CODE_RE = re.compile('/translate/languages/([\w\-]+)')


class NoSupportedSubtitleLanguagesFound(Exception):
    pass


def get_supported_subtitle_languages():
    logging.debug('Looking for supported subtitle languages...')
    document = html.parse(LANGUAGES_LIST_URL)
    
    languages = {}
    for a in _LANGUAGES_SELECTOR(document):
        language_name = a.get('title')
        match = _LANGUAGE_CODE_RE.search(a.get('href'))
        if match:
            languages[match.group(1)] = language_name
        else:
            logging.warning("'%s' doesn't seem to be a language", language_name)
    
    if not languages:
        raise NoSupportedSubtitleLanguagesFound('No supported subtitle languages found')
    
    logging.info("Found %d supported subtitle language(s)", len(languages))
    logging.debug("Supported subtitle languages are: %s", languages)
    return languages
