"""setup script for cheater"""

from distutils.core import setup
import os

setup(
    name='cheater',
    version='0.1.20170721',
    author='Florian Poeck',
    author_email='fidel@yafp.de',
    license='GPL3',
    description='cheater allows you to create and view interactive cheatsheets '
    'on the command-line. It was designed to help remind *nix system '
    'administrators of options for commands that they use frequently, but not '
    'frequently enough to remember.',
    url='https://github.com/yafp/cheater',
    packages=[
        'cheater',
        'cheater.cheatsheets',
        'cheater.test',
    ],
    package_data={
        'cheater.cheatsheets': [f for f in os.listdir('cheater/cheatsheets') if '.' not in f]
    },
    scripts=['bin/cheater'],
    install_requires=[
        'docopt >= 0.6.1',
        'pygments >= 1.6.0',
    ]
)
