# -*- coding: utf-8 -*-
import logging
from lxml import html
from lxml.cssselect import CSSSelector
from lxml.etree import XPath
import re
from urlparse import urljoin
from .. import SITE_URL


_HTML_ENTITY_RE = re.compile(r'&(#?[xX]?[0-9a-fA-F]+|\w{1,8});')
_INVALID_FILE_NAME_CHARS_RE = re.compile('[^\w\.\- ]+')

_EXTERNALLY_HOSTED_DOWNLOADS_SELECTOR = CSSSelector('div#external_player')

_AUTHOR_BIO_XPATH = XPath(u'//a[contains(text(), "Full bio")]')

_EVENT_SELECTOR = CSSSelector('div.talk-meta span.event-name')

_TRANSCRIPT_LANGUAGES_SELECTOR = CSSSelector('select#languageCode option')

_VIDEO_PLAYER_INFO_SELECTOR = CSSSelector('div#maincontent > div.leftColumn > script')
_MEDIA_SLUG_RE = re.compile('"mediaSlug":"(\w+)"')

AVAILABLE_VIDEO_QUALITIES = {
    'low': '-low',
    'high': '-480p',
}

_YEARS_SELECTOR = CSSSelector('div.talk-meta')
_YEARS_RE_DICT = {
    'filming_year': re.compile('Filmed \w+ (\d+)'),
    'publishing_year': re.compile('Posted \w+ (\d+)'),
}


class NoDownloadsFound(Exception):
    pass


class ExternallyHostedDownloads(Exception):
    pass


def _clean_up_file_name(file_name, replace_first_colon_with_dash=False):
    if replace_first_colon_with_dash:
        # Turns 'Barry Schuler: Genomics' into 'Barry Schuler - Genomics'
        file_name = file_name.replace(': ', ' - ', 1)
    # Remove html entities
    file_name = _HTML_ENTITY_RE.sub('', file_name)
    # Remove invalid file name characters
    file_name = _INVALID_FILE_NAME_CHARS_RE.sub('', file_name)
    # Should be clean now
    return file_name

def _guess_author(talk_url, document):
    """
    Tries to guess the author, or returns 'Unknown' if no author was found.
    """
    elements = _AUTHOR_BIO_XPATH(document)
    if elements:
        author_bio_url = urljoin(SITE_URL, elements[0].get('href'))
        author_bio_document = html.parse(author_bio_url)
        return _clean_up_file_name(
            author_bio_document.find('/head/title').text.split('|')[0].strip()
        )
    
    logging.warning("Failed to guess the author of '%s'", talk_url)
    return 'Unknown'

def _guess_event(talk_url, document):
    """
    Tries to guess the talks event, or returns 'Unknown' if no event was found.
    """
    elements = _EVENT_SELECTOR(document)
    if elements:
        return _clean_up_file_name(elements[0].text)
    
    logging.warning("Failed to guess the event of '%s'", talk_url)
    return 'Unknown'

def _get_subtitle_languages_codes(talk_url, document):
    """
    Returns a list of all subtitle language codes for a given talk URL. 
    """
    language_codes = [
        opt.get('value')
        for opt in _TRANSCRIPT_LANGUAGES_SELECTOR(document)
        if opt.get('value') != ''
    ]
    
    if not language_codes:
        logging.warning("Failed to find any subtitles for '%s'", talk_url)
    
    return language_codes

def _get_media_slug(talk_url, document):
    elements = _VIDEO_PLAYER_INFO_SELECTOR(document)
    if elements:
        match = _MEDIA_SLUG_RE.search(elements[0].text)
        if match:
            return match.group(1)
    
    raise NoDownloadsFound(talk_url)

def _get_file_base_name(document):
    return _clean_up_file_name(
        document.find('/head/title').text.split('|')[0].strip(),
        replace_first_colon_with_dash=True
    )

def _guess_year(name, regexp, talk_url, document):
    elements = _YEARS_SELECTOR(document)
    if elements:
        match = regexp.search(elements[0].text_content())
        if match:
            return _clean_up_file_name(match.group(1))
    
    logging.warning("Failed to guess the %s of '%s'", name, talk_url)
    return 'Unknown'

def get_talk_info(talk_url):
    document = html.parse(talk_url)
    
    # Downloads not hosted by TED!
    if _EXTERNALLY_HOSTED_DOWNLOADS_SELECTOR(document):
        raise ExternallyHostedDownloads(talk_url)
    
    talk_info = {
        'author': _guess_author(talk_url, document),
        'event': _guess_event(talk_url, document),
        'language_codes': _get_subtitle_languages_codes(talk_url, document),
        'media_slug': _get_media_slug(talk_url, document),
        'file_base_name': _get_file_base_name(document),
    }
    talk_info.update(
        (name, _guess_year(name, regexp, talk_url, document))
        for name, regexp in _YEARS_RE_DICT.items()
    )
    return talk_info
