from distribute_setup import use_setuptools
use_setuptools() 

import sys
from setuptools import setup, find_packages


import metaTED


if sys.version_info < (2, 6):
    print 'ERROR: metaTED requires at least Python 2.6 to run.'
    sys.exit(1)


setup(
    name='metaTED',
    version=metaTED.__version__,
    url='http://bitbucket.org/petar/metated/',
    download_url='http://pypi.python.org/pypi/metaTED',
    license='BSD',
    author='Petar Maric',
    author_email='petar.maric@gmail.com',
    description='Creates metalink files of TED talks for easier downloading',
    long_description=open('README').read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Utilities',
    ],
    keywords='TED metalink download video',
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['metaTED=metaTED:main']
    },
    install_requires=open('requirements.txt').read().splitlines()
)
