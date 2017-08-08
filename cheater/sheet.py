"""sheet for cheater"""

# general imports
import os
import shutil

# cheater imports
import cheater.utils as u
import cheater.constants as c
from cheater import sheets
from cheater.utils import die, open_with_editor

def copy(current_sheet_path, new_sheet_path):
    """ Copies a sheet to a new path """
    u.debug_output(__name__, 'Function: copy()')

    # attempt to copy the sheet to DEFAULT_CHEATER_DIR
    try:
        shutil.copy(current_sheet_path, new_sheet_path)

    # fail gracefully if the cheatsheet cannot be copied. This can happen if
    # DEFAULT_CHEATER_DIR does not exist
    except IOError:
        die('Could not copy cheatsheet for editing.')


def create_or_edit(sheet):
    """ Creates or edits a cheatsheet """
    u.debug_output(__name__, 'Function: create_or_edit()')

    # if the cheatsheet does not exist
    if not exists(sheet):
        u.debug_output(__name__, 'Cheatsheet ' + sheet + ' does not exist, need to create it')
        create(sheet)

    # if the cheatsheet exists but not in the default_path, copy it to the
    # default path before editing
    elif exists(sheet) and not exists_in_default_path(sheet):
        u.debug_output(__name__, 'Cheatsheet ' + sheet + ' exists, but not in the default path')
        u.debug_output(__name__, 'Copying cheatsheet ' + sheet + ' to default path')
        copy(path(sheet), os.path.join(sheets.default_path(), sheet))
        edit(sheet)

    # if it exists and is in the default path, then just open it
    else:
        u.debug_output(__name__, 'Cheatsheet ' + sheet + ' exists in the default path')
        edit(sheet)


def create(sheet):
    """ Creates a cheatsheet """
    u.debug_output(__name__, 'Function: create()')
    new_sheet_path = os.path.join(sheets.default_path(), sheet)
    open_with_editor(new_sheet_path)


def edit(sheet):
    """ Opens a cheatsheet for editing """
    u.debug_output(__name__, 'Function: edit()')
    open_with_editor(path(sheet))


def exists(sheet):
    """ Predicate that returns true if the sheet exists """
    u.debug_output(__name__, 'Function: exists()')
    return sheet in sheets.get() and os.access(path(sheet), os.R_OK)


def exists_in_default_path(sheet):
    """ Predicate that returns true if the sheet exists in default_path"""
    u.debug_output(__name__, 'Function: exists_in_default_path()')
    default_path_sheet = os.path.join(sheets.default_path(), sheet)
    return sheet in sheets.get() and os.access(default_path_sheet, os.R_OK)


def is_writable(sheet):
    """ Predicate that returns true if the sheet is writeable """
    u.debug_output(__name__, 'Function: is_writeable()')
    return sheet in sheets.get() and os.access(path(sheet), os.W_OK)


def path(sheet):
    """ Returns a sheet's filesystem path """
    u.debug_output(__name__, 'Function: path()')
    return sheets.get()[sheet]


def read(sheet):
    """ Returns the contents of the cheatsheet as a String """
    u.debug_output(__name__, 'Function: read()')
    if not exists(sheet): # sheet does not exist
        u.debug_output(__name__, 'Cheatsheet '+ sheet +' not found', 1)
        die('No cheatsheet found with the name \033[01m'+c.FONT_BOLD + c.FONT_GREEN + sheet + c.FONT_RESET+'.\n')

    with open(path(sheet)) as cheatfile:
        print c.FONT_BOLD+'Location: '+c.FONT_RESET + path(sheet) +'\n' # Issue #3
        u.debug_output(__name__, 'finished reading cheatsheet')
        return cheatfile.read()
