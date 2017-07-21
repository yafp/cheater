"""sheets for cheater"""

# general imports
import os

# cheater imports
import cheater.utils as u
import cheater.constants as c
from cheater import cheatsheets
from cheater.utils import die


def default_path():
    """ Returns the default cheatsheet path """
    u.debug_output(__name__, 'Function: default_path()')

    # determine the default cheatsheet dir
    default_sheets_dir = os.environ.get('DEFAULT_CHEATER_DIR') or os.path.join('~', '.cheater')

    # enhance users default path from ~/.cheater to /home/USERNAME/+cheater
    default_sheets_dir = os.path.expanduser(os.path.expandvars(default_sheets_dir))
    u.debug_output(__name__, 'Got local user path: ' + default_sheets_dir)

    # create the DEFAULT_CHEATER_DIR if it does not exist
    if not os.path.isdir(default_sheets_dir):
        try:
            # @kludge: unclear on why this is necessary
            os.umask(0000)
            os.mkdir(default_sheets_dir)

        except OSError:
            u.debug_output(__name__, 'Could not create default cheat dir', 2)
            die('Could not create DEFAULT_CHEATER_DIR')

    # assert that the DEFAULT_CHEATER_DIR is readable and writable
    if not os.access(default_sheets_dir, os.R_OK):
        u.debug_output(__name__, 'The DEFAULT_CHEATER_DIR (' + default_sheets_dir +') is not readable.', 2)
        die('The DEFAULT_CHEATER_DIR (' + default_sheets_dir +') is not readable.')

    if not os.access(default_sheets_dir, os.W_OK):
        u.debug_output(__name__, 'The DEFAULT_CHEATER_DIR (' + default_sheets_dir +') is not writable.', 2)
        die('The DEFAULT_CHEATER_DIR (' + default_sheets_dir +') is not writable.')

    # return the default dir
    return default_sheets_dir


def get():
    """ Assembles a dictionary of cheatsheets as name => file-path """
    u.debug_output(__name__, 'Function: get()')

    cheats = {}

    # otherwise, scan the filesystem
    for cheat_dir in reversed(paths()):
        cheats.update(
            dict([
                (cheat, os.path.join(cheat_dir, cheat))
                for cheat in os.listdir(cheat_dir)
                if not cheat.startswith('.')
                and not cheat.startswith('__')
            ])
        )

    return cheats


def paths():
    """ Assembles a list of directories containing cheatsheets """
    u.debug_output(__name__, 'Function: paths()')

    sheet_paths = [
        default_path(),
        cheatsheets.sheets_dir()[0],
    ]

    # merge the CHEATERPATH paths into the sheet_paths
    if 'CHEATERPATH' in os.environ and os.environ['CHEATERPATH']:
        for path in os.environ['CHEATERPATH'].split(os.pathsep):
            if os.path.isdir(path):
                sheet_paths.append(path)

    if not sheet_paths:
        u.debug_output(__name__, 'The DEFAULT_CHEATER_DIR dir does not exist or the CHEATERPATH is not set.', 2)
        die('The DEFAULT_CHEATER_DIR dir does not exist or the CHEATERPATH is not set.')

    return sheet_paths


def list():
    """ Lists the available cheatsheets """
    u.debug_output(__name__, 'Function: list()')
    u.debug_output(__name__, 'Going to list all existing cheatsheets (sorted by name)')

    sheetcounter = 0 # int variable to count amount of matches

    sheet_list = ''
    pad_length = max([len(x) for x in get().keys()]) + 4

    # store all sheet names and locations into sheet_list
    for sheet in sorted(get().items()):
        sheetcounter = sheetcounter + 1
        sheet_list += sheet[0].ljust(pad_length) + sheet[1] + "\n"

    # add header
    sheet_list = "CHEATSHEET".ljust(pad_length) + "LOCATION\n\n" + sheet_list

    # add footer
    sheet_list = sheet_list + '\n\nFound '  + c.FONT_BOLD + c.FONT_GREEN + str(sheetcounter) + c.FONT_RESET+' cheatsheets.\n'

    u.debug_output(__name__, 'Found '+str(sheetcounter)+' cheatsheets')

    # return
    return sheet_list


def search(term):
    """ Searches all cheatsheets for the specified term """
    u.debug_output(__name__, 'Function: search()')

    result = '' # string variable which contains the actual result-text
    sheetcounter = 0 # int variable to count amount of matching cheatsheets
    linecounter = 0 # int variable to count occurences in single lines 

    u.debug_output(__name__, 'Starting search over all cheatsheets for the term: "'+ term +'"')

    for cheatsheet in sorted(get().items()): # for all cheatsheets
        match = '' # string variable which later may contains the matching line
        sheetscore = 0 # int variable to count score of each sheet

        for line in open(cheatsheet[1]): # check all lines of current cheatsheet
            #if term in line:
            if term.lower() in line.lower(): # search should not be case-specific

                # count how often line contains searchstring
                sheetscore = sheetscore + line.count(term)

                # highlight search term in current line
                highlight = c.FONT_BG_ORANGE + c.FONT_BLACK + term + c.FONT_RESET # contruct highlighted text
                line = line.replace(term, highlight) # replace it

                # attach line to match-text
                match += '  ' + line

                # update result counter
                linecounter = linecounter + line.count(term)


        # if we got a match - add name of related sheet and all lines which match
        if match != '':
            # Colored and including path to sheet
            result += ' [' + c.FONT_GREEN + str(sheetscore)+ c.FONT_RESET + '] '+ \
                c.FONT_BOLD + c.FONT_BLUE + cheatsheet[0] + ':' + \
                c.FONT_RESET+ ' ('+ cheatsheet[1] +')\n' + \
                match + '\n' # name of cheatsheet + complete path to cheatsheet + maching lines in cheatsheet

            # update sheet counter
            sheetcounter = sheetcounter + 1

    u.debug_output(__name__, 'Finished search over all cheatsheets for the term: "' + term + '"')
    u.debug_output(__name__, 'Found ' + str(linecounter) + ' matches in '+ str(sheetcounter) + ' cheatsheets')

    # add result footer
    result = result + '\n Your search for ' + c.FONT_BOLD + c.FONT_GREEN + term + c.FONT_RESET + \
        ' resulted in ' + c.FONT_BOLD + c.FONT_GREEN + str(linecounter) + c.FONT_RESET + \
        ' matches in ' + c.FONT_BOLD+c.FONT_GREEN + str(sheetcounter) + c.FONT_RESET + ' cheatsheets\n\n'

    return result
