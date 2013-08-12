from email.utils import formatdate
from jinja2 import Environment, PackageLoader
import logging
from multiprocessing import Pool
import os
from . import __version__
from .cache import cached_storage
from .crawler.get_downloadable_talks import get_downloadable_talks
from .crawler.get_supported_subtitle_languages import get_supported_subtitle_languages
from .crawler.get_talk_info import AVAILABLE_VIDEO_QUALITIES


_METALINK_BASE_URL = "http://metated.petarmaric.com/metalinks/%s"


def _get_metalink_file_name(language_code, quality, group_by):
    return "TED-talks%s-in-%s-quality.%s.metalink" % (
        "-grouped-by-%s" % group_by.replace('_', '-') if group_by else '',
        quality,
        language_code
    )

def _get_metalink_description(language_name, quality, group_by):
    return "Download TED talks with %s subtitles%s encoded in %s quality" % (
        language_name,
        " grouped by %s" % group_by.replace('_', ' ') if group_by else '',
        quality
    )

def _get_group_downloads_by(downloadable_talks):
    groups = [None] # Also generate metalinks with no grouped downloads
    
    # Extract talk_info metadata and guess possible groupings from it
    groups.extend(downloadable_talks[0].keys())
    
    groups.remove('language_codes') # Can't group by subtitle languages metadata
    groups.remove('media_slug') # Can't group by media slug metadata
    groups.remove('file_base_name') # Can't group by file name
    
    groups.sort()
    
    logging.debug("Downloads can be grouped by '%s'", groups)
    return groups

_metalink_worker_immutable_data_cache = {}
def _init_metalink_worker_immutable_data_cache(*data):
    global _metalink_worker_immutable_data_cache
    
    data_keys = 'output_dir, downloadable_talks, first_published_on, refresh_date'.split(', ')
    _metalink_worker_immutable_data_cache = dict(zip(data_keys, data))
    
    # Prepare the template upfront, because it can be reused by the same worker
    # process for multiple metalinks
    env = Environment(loader=PackageLoader('metaTED'))
    _metalink_worker_immutable_data_cache['template'] = env.get_template(
        'template.metalink'
    )

def _generate_metalink(args):
    language_code, language_name, group_by, quality = args
    c = _metalink_worker_immutable_data_cache
    
    metalink_file_name = _get_metalink_file_name(language_code, quality, group_by)
    metalink_url = _METALINK_BASE_URL % metalink_file_name
    metalink_description = _get_metalink_description(language_name, quality, group_by)
    logging.debug("Generating '%s' metalink...", metalink_file_name)
    c['template'].stream({
        'metalink_url': metalink_url,
        'metaTED_version': __version__,
        'first_published_on': c['first_published_on'],
        'refresh_date': c['refresh_date'],
        'description': metalink_description,
        'downloadable_talks': c['downloadable_talks'],
        'language_code': language_code,
        'group_by': group_by,
        'quality_slug': AVAILABLE_VIDEO_QUALITIES[quality],
    }).dump(
        os.path.join(c['output_dir'], metalink_file_name),
        encoding='utf-8'
    )
    logging.info("Generated '%s' metalink", metalink_file_name)
    return {
        'language_code': language_code,
        'language_name': language_name,
        'download_url': metalink_url,
        'description': metalink_description,
    }

def generate_metalinks(output_dir=None):
    output_dir = os.path.abspath(output_dir or '')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Make sure downloadable_talks can be calculated
    downloadable_talks = get_downloadable_talks().values()
    
    # Use the same dates/times for all metalinks because they should, in my
    # opinion, point out when the metalinks were being generated and not when
    # they were physically written do disk
    refresh_date = formatdate()
    first_published_on = cached_storage.get('first_published_on')
    if first_published_on is None:
        cached_storage['first_published_on'] = first_published_on = refresh_date
    
    # Generate all metalink variants
    group_by_list = _get_group_downloads_by(downloadable_talks)
    variants = [
        (language_code, language_name, group_by, quality)
        for language_code, language_name in get_supported_subtitle_languages().items()
            for group_by in group_by_list
                for quality in AVAILABLE_VIDEO_QUALITIES.keys()
    ]
    metalinks = Pool(
        initializer=_init_metalink_worker_immutable_data_cache,
        initargs=(output_dir, downloadable_talks, first_published_on, refresh_date)
    ).map(
        func=_generate_metalink,
        iterable=variants,
    )
    
    return {
        'metaTED_version': __version__,
        'first_published_on': first_published_on,
        'refresh_date': refresh_date,
        'num_downloadable_talks': len(downloadable_talks),
        'metalinks': metalinks
    }
