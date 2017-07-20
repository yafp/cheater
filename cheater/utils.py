"""utils for cheater"""

# general imports
from __future__ import print_function
import datetime # for timestamp
import os
import sys
import subprocess

# cheater imports
import cheater.constants as c


def debug_output(source, message):
    """ Output debugging informations if CONST is set to TRUE """
    if c.DEBUG is True:
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        print(c.FONT_BOLD + c.FONT_RED + 'DEBUG: ' + c.FONT_RESET + c.FONT_GREEN + timestamp + c.FONT_RESET+' >> source: ' + c.FONT_PURPLE + source + c.FONT_RESET +' msg: '+ c.FONT_PURPLE + message + c.FONT_RESET)


def clear_terminal():
    """ Clears the terminal """
    print(chr(27) + "[2J")  # clear terminal[2J")  # clear terminal


def colorize(sheet_content):
    """ Colorizes cheatsheet content if so configured """
    debug_output(__name__, 'Starting colorize()')

    # only colorize if so configured
    #if not 'CHEATCOLORS' in os.environ:
    if 'CHEATCOLORS' not in os.environ:
        return sheet_content

    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import TerminalFormatter

    # if pygments can't load, just return the uncolorized text
    except ImportError:
        return sheet_content

    first_line = sheet_content.splitlines()[0]
    lexer = get_lexer_by_name('bash')
    if first_line.startswith('```'):
        sheet_content = '\n'.join(sheet_content.split('\n')[1:-2])
        try:
            lexer = get_lexer_by_name(first_liine[3:])
        except Exception:
            pass

    return highlight(sheet_content, lexer, TerminalFormatter())


def die(message):
    """ Prints a message to stderr and then terminates """
    debug_output(__name__, 'Starting die() to display a message to stderr and then terminate')

    warn(message)
    exit(1)


def editor():
    """ Determines the user's preferred editor """
    debug_output(__name__, 'Starting editor()')

    # determine which editor to use
    editor = os.environ.get('CHEATER_EDITOR') \
        or os.environ.get('VISUAL')         \
        or os.environ.get('EDITOR')         \
        or False

    # assert that the editor is set
    if editor is False:
        die(
            'You must set a CHEAT_EDITOR, VISUAL, or EDITOR environment '
            'variable in order to create/edit a cheatsheet.'
        )

    return editor


def open_with_editor(filepath):
    """ Open `filepath` using the EDITOR specified by the environment variables """
    debug_output(__name__, 'Starting open_with_editor()')

    editor_cmd = editor().split()
    try:
        subprocess.call(editor_cmd + [filepath])
    except OSError:
        die('Could not launch ' + editor())


def warn(message):
    """ Prints a message to stderr """
    debug_output(__name__, 'Starting warn()')

    print((message), file=sys.stderr)
