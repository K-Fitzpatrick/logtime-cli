"""
Manipulate and manage configuration files.
"""

import ConfigParser
from os import path, system

DEFAULT_CONFIG_FILE = path.dirname(__file__) + '/config/config-default.ini'
USER_CONFIG_FILE = path.dirname(__file__) + '/config/config-user.ini'

_DEFAULT_CONFIG = ConfigParser.ConfigParser()
_DEFAULT_CONFIG.read(DEFAULT_CONFIG_FILE)

_USER_CONFIG = ConfigParser.ConfigParser()
_USER_CONFIG.read(USER_CONFIG_FILE)


def get_option(section, name):
    """
    Retrieve an option from the config files.
    First, check User Config
    If the options doesn't exist there, check Default Config
    """
    if _USER_CONFIG.has_option(section, name):
        return _USER_CONFIG.get(section, name)
    return _DEFAULT_CONFIG.get(section, name)


def _create_user_config():
    config_file = open(USER_CONFIG_FILE, 'w')
    _DEFAULT_CONFIG.write(config_file)
    config_file.close()
    _USER_CONFIG.read(USER_CONFIG_FILE)


def open_user_config():
    """
    Opens the User Config file with the user's default text editor
    """
    if not path.isfile(USER_CONFIG_FILE):
        _create_user_config()
    system("start " + USER_CONFIG_FILE)
    exit()
