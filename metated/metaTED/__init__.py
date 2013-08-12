SITE_URL = 'http://www.ted.com/'

__version__ = '2.1.0'


def main():
    # Setup command line option parser
    import logging
    from optparse import OptionParser
    parser = OptionParser(prog='metaTED', version=__version__)
    parser.add_option(
        '-q',
        '--quiet',
        action='store_const',
        const=logging.WARN,
        dest='verbosity',
        help='Be quiet, show only warnings and errors'
    )
    parser.add_option(
        '-v',
        '--verbose',
        action='store_const',
        const=logging.DEBUG,
        dest='verbosity',
        help='Be very verbose, show debug information'
    )
    parser.add_option(
        '-o',
        '--output-directory',
        dest='output_dir',
        help='Write generated metalinks to specified output directory'
    )
    (options, _) = parser.parse_args()
    
    # Configure logging
    log_level = options.verbosity or logging.INFO
    logging.basicConfig(level=log_level, format="[%(levelname)s] %(message)s")
    
    # Generate metalinks
    from metaTED.metalink import generate_metalinks
    generate_metalinks(options.output_dir)

if __name__ == '__main__':
    main()
