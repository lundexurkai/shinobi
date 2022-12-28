r"""
Evennia settings file.

The available options are found in the default settings file found
here:

/home/kai/muddev/evennia/evennia/settings_default.py

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

# This is the name of your game. Make it catchy!
SERVERNAME = "Shinobi"


######################################################################
# Evennia pluggable modules
######################################################################
# Plugin modules extend Evennia in various ways. In the cases with no
# existing default, there are examples of many of these modules
# in contrib/examples.

# On a multi-match when search objects or commands, the user has the
# ability to search again with an index marker that differentiates
# the results. If multiple "box" objects
# are found, they can by default be separated as 1-box, 2-box. Below you
# can change the regular expression used. The regex must have one
# have two capturing groups (?P<number>...) and (?P<name>...) - the default
# parser expects this. It should also involve a number starting from 1.
# When changing this you must also update SEARCH_MULTIMATCH_TEMPLATE
# to properly describe the syntax.
SEARCH_MULTIMATCH_REGEX = r"(?P<name>[^-]*)-(?P<number>[0-9]+)(?P<args>.*)"
# To display multimatch errors in various listings we must display
# the syntax in a way that matches what SEARCH_MULTIMATCH_REGEX understand.
# The template will be populated with data and expects the following markup:
# {number} - the order of the multimatch, starting from 1; {name} - the
# name (key) of the multimatched entity; {aliases} - eventual
# aliases for the entity; {info} - extra info like #dbrefs for staff. Don't
# forget a line break if you want one match per line.
SEARCH_MULTIMATCH_TEMPLATE = " {name}-{number}{aliases}{info}\n"
# The module holding text strings for the connection screen.
# This module should contain one or more variables
# with strings defining the look of the screen.
# CONNECTION_SCREEN_MODULE = "server.conf.connection_screens"
CONNECTION_SCREEN_MODULE = "evennia.contrib.base_systems.menu_login.connection_screens"
# Modules that contain prototypes for use with the spawner mechanism.
PROTOTYPE_MODULES = ["world.prototypes"]
# Modules containining Prototype functions able to be embedded in prototype
# definitions from in-game.
PROT_FUNC_MODULES = ["evennia.prototypes.protfuncs"]
######################################################################
# Default command sets and commands
######################################################################

# Command set used on session before account has logged in
# CMDSET_UNLOGGEDIN = "commands.default_cmdsets.UnloggedinCmdSet"
CMDSET_UNLOGGEDIN = "evennia.contrib.base_systems.menu_login.UnloggedinCmdSet"
# Parent class for all default commands. Changing this class will
# modify all default commands, so do so carefully.
# COMMAND_DEFAULT_CLASS = "evennia.commands.default.muxcommand.MuxCommand"
COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"


######################################################################
# Batch processors
######################################################################

# Python path to a directory to be searched for batch scripts
# for the batch processors (.ev and/or .py files).
BASE_BATCHPROCESS_PATHS = [
    "world",
    "evennia.contrib",
    "evennia.contrib.tutorials",
]


######################################################################
# Typeclasses and other paths
######################################################################

# These are paths that will be prefixed to the paths given if the
# immediately entered path fail to find a typeclass. It allows for
# shorter input strings. They must either base off the game directory
# or start from the evennia library.
TYPECLASS_PATHS += [
    "typeclasses.accounts",
    "typeclasses.channels",
    "typeclasses.characters",
    "typeclasses.objects",
    "typeclasses.rooms",
    "typeclasses.scripts",
]

# Typeclass for account objects (linked to a character) (fallback)
BASE_ACCOUNT_TYPECLASS = "typeclasses.accounts.accounts.Account"
BASE_GUEST_TYPECLASS = "typeclasses.accounts.accounts.Guest"

# Typeclass and base for all objects (fallback)
BASE_OBJECT_TYPECLASS = "typeclasses.objects.objects.Object"
# Typeclass for character objects linked to an account (fallback)
BASE_CHARACTER_TYPECLASS = "typeclasses.characters.characters.Character"
# Typeclass for rooms (fallback)
BASE_ROOM_TYPECLASS = "typeclasses.rooms.rooms.Room"
# Typeclass for Exit objects (fallback).
BASE_EXIT_TYPECLASS = "typeclasses.rooms.exits.Exit"
# Typeclass for Channel (fallback).
BASE_CHANNEL_TYPECLASS = "typeclasses.channels.channels.Channel"
# Typeclass for Scripts (fallback). You usually don't need to change this
# but create custom variations of scripts on a per-case basis instead.
BASE_SCRIPT_TYPECLASS = "typeclasses.scripts.scripts.Script"
# The default home location used for all objects. This is used as a
# fallback if an object's normal home location is deleted. Default
# is Limbo (#2).
DEFAULT_HOME = "#2"
# The start position for new characters. Default is Limbo (#2).
START_LOCATION = "#2"


######################################################################
# Game Time setup
######################################################################

# You don't actually have to use this, but it affects the routines in
# evennia.utils.gametime.py and allows for a convenient measure to
# determine the current in-game time. You can of course interpret
# "week", "month" etc as your own in-game time units as desired.

# The time factor dictates if the game world runs faster (timefactor>1)
# or slower (timefactor<1) than the real world.
TIME_FACTOR = 2.0
# The starting point of your game time (the epoch), in seconds.
# In Python a value of 0 means Jan 1 1970 (use negatives for earlier
# start date). This will affect the returns from the utils.gametime
# module. If None, the server's first start-time is used as the epoch.
TIME_GAME_EPOCH = None
# Normally, game time will only increase when the server runs. If this is True,
# game time will not pause when the server reloads or goes offline. This setting
# together with a time factor of 1 should keep the game in sync with
# the real time (add a different epoch to shift time)
TIME_IGNORE_DOWNTIMES = False

######################################################################
# Global Scripts
######################################################################

# Global scripts started here will be available through
# 'evennia.GLOBAL_SCRIPTS.key'. The scripts will survive a reload and be
# recreated automatically if deleted. Each entry must have the script keys,
# whereas all other fields in the specification are optional. If 'typeclass' is
# not given, BASE_SCRIPT_TYPECLASS will be assumed.  Note that if you change
# typeclass for the same key, a new Script will replace the old one on
# `evennia.GLOBAL_SCRIPTS`.
GLOBAL_SCRIPTS = {
    # 'key': {'typeclass': 'typeclass.path.here',
    #         'repeats': -1, 'interval': 50, 'desc': 'Example script'},
}

######################################################################
# Default Account setup and access
######################################################################

# Different Multisession modes allow a player (=account) to connect to the
# game simultaneously with multiple clients (=sessions).
#  0 - single session per account (if reconnecting, disconnect old session)
#  1 - multiple sessions per account, all sessions share output
#  2 - multiple sessions per account, one session allowed per puppet
#  3 - multiple sessions per account, multiple sessions per puppet (share output)
#      session getting the same data.
MULTISESSION_MODE = 0
# Whether we should create a character with the same name as the account when
# a new account is created. Together with AUTO_PUPPET_ON_LOGIN, this mimics
# a legacy MUD, where there is no difference between account and character.
AUTO_CREATE_CHARACTER_WITH_ACCOUNT = False
# Whether an account should auto-puppet the last puppeted puppet when logging in. This
# will only work if the session/puppet combination can be determined (usually
# MULTISESSION_MODE 0 or 1), otherwise, the player will end up OOC. Use
# MULTISESSION_MODE=0, AUTO_CREATE_CHARACTER_WITH_ACCOUNT=True and this value to
# mimic a legacy mud with minimal difference between Account and Character. Disable
# this and AUTO_PUPPET to get a chargen/character select screen on login.
AUTO_PUPPET_ON_LOGIN = False
# How many *different* characters an account can puppet *at the same time*. A value
# above 1 only makes a difference together with MULTISESSION_MODE > 1.
MAX_NR_SIMULTANEOUS_PUPPETS = 1
# The maximum number of characters allowed by be created by the default ooc
# char-creation command. This can be seen as how big of a 'stable' of characters
# an account can have (not how many you can puppet at the same time). Set to
# None for no limit.
MAX_NR_CHARACTERS = 1
# The access hierarchy, in climbing order. A higher permission in the
# hierarchy includes access of all levels below it. Used by the perm()/pperm()
# lock functions, which accepts both plural and singular (Admin & Admins)
PERMISSION_HIERARCHY = [
    "Guest",  # note-only used if GUEST_ENABLED=True
    "Player",
    "Helper",
    "Builder",
    "Admin",
    "Developer",
]
# The default permission given to all new accounts
PERMISSION_ACCOUNT_DEFAULT = "Player"
# Default sizes for client window (in number of characters), if client
# is not supplying this on its own
CLIENT_DEFAULT_WIDTH = 78
# telnet standard height is 24; does anyone use such low-res displays anymore?
CLIENT_DEFAULT_HEIGHT = 45
# Set rate limits per-IP on account creations and login attempts. Set limits
# to None to disable.
CREATION_THROTTLE_LIMIT = 2
CREATION_THROTTLE_TIMEOUT = 10 * 60
LOGIN_THROTTLE_LIMIT = 5
LOGIN_THROTTLE_TIMEOUT = 5 * 60
# Certain characters, like html tags, line breaks and tabs are stripped
# from user input for commands using the `evennia.utils.strip_unsafe_input` helper
# since they can be exploitative. This list defines Account-level permissions
# (and higher) that bypass this stripping. It is used as a fallback if a
# specific list of perms are not given to the helper function.
INPUT_CLEANUP_BYPASS_PERMISSIONS = ["Builder"]


BACKGROUND_MODULE = "shinobi.backgrounds.default"
MODIFIER_MODULE = "shinobi.modifiers.default"

######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
