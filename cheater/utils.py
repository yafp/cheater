"""utils for cheater"""

# general imports
from __future__ import print_function
import datetime # for timestamp
import os
import sys
import subprocess

# cheater imports
import cheater.constants as c


def debug_output(source, message, message_type=0):
    """
        Output debugging informations if CONST is set to TRUE
        message_type: 0 = normal (default)
        message_type: 1 = warning
        message_type: 2 = error
    """
    if c.DEBUG is True:
        # define message type & color
        if(message_type == 2): # Error
            text_color = c.FONT_RED
            message_type_class = ' E '

        elif(message_type == 1): # Warning
            text_color = c.FONT_YELLOW
            message_type_class = ' W '

        else: # Default = Info
            text_color = c.FONT_GREEN
            message_type_class = ' I '

        # generate a timestamp
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

        # output debug message
        print(c.FONT_BOLD + c.FONT_RED + 'DEBUG: ' + c.FONT_RESET + text_color + message_type_class + c.FONT_RESET + " # " + c.FONT_GREEN + timestamp + c.FONT_RESET+' >> source: ' + c.FONT_PURPLE + source + c.FONT_RESET +' msg: '+ c.FONT_PURPLE + message + c.FONT_RESET)


def clear_terminal():
    """ Clears the terminal """
    print(chr(27) + "[2J")  # clear terminal


def colorize(sheet_content):
    """ Colorizes cheatsheet content if so configured """
    debug_output(__name__, 'Function: colorize()')

    # only colorize if so configured
    #if not 'CHEATCOLORS' in os.environ:
    if 'CHEATCOLORS' not in os.environ:
        debug_output(__name__, 'CHEATCOLORS not in env', 1)
        return sheet_content

    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import TerminalFormatter

    # if pygments can't load, just return the uncolorized text
    except ImportError:
        debug_output(__name__, 'Unable to colorize content of sheet', 1)
        return sheet_content

    debug_output(__name__, 'Colorizing ...')
    first_line = sheet_content.splitlines()[0]
    lexer = get_lexer_by_name('bash')
    if first_line.startswith('```'):
        sheet_content = '\n'.join(sheet_content.split('\n')[1:-2])
        try:
            lexer = get_lexer_by_name(first_liine[3:])
        except Exception:
            pass
    debug_output(__name__, 'Finished colorizing')

    return highlight(sheet_content, lexer, TerminalFormatter())


def die(message):
    """ Prints a message to stderr and then terminates """
    debug_output(__name__, 'Function: die()')

    warn(message)
    exit(1)


def editor():
    """ Determines the user's preferred editor """
    debug_output(__name__, 'Function: editor()')

    # determine which editor to use
    editor = os.environ.get('CHEATER_EDITOR') \
        or os.environ.get('VISUAL')         \
        or os.environ.get('EDITOR')         \
        or False

    # assert that the editor is set
    if editor is False:
        debug_output(__name__, 'Editor is not set')
        die(
            'You must set a CHEAT_EDITOR, VISUAL, or EDITOR environment '
            'variable in order to create/edit a cheatsheet.'
        )

    return editor


def open_with_editor(filepath):
    """ Open `filepath` using the EDITOR specified by the environment variables """
    debug_output(__name__, 'function: open_with_editor()')

    editor_cmd = editor().split()
    try:
        subprocess.call(editor_cmd + [filepath])
    except OSError:
        die('Could not launch ' + editor())


def warn(message):
    """ Prints a message to stderr """
    debug_output(__name__, 'Function: warn()')

    # show warn message
    print((message), file=sys.stderr)
