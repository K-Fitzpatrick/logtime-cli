import ConfigParser
from os import path, system

DEFAULT_CONFIG_FILE = path.dirname(__file__) + '/config/config-default.ini'
USER_CONFIG_FILE = path.dirname(__file__) + '/config/config-user.ini'

_DEFAULT_CONFIG = ConfigParser.ConfigParser()
_DEFAULT_CONFIG.read(DEFAULT_CONFIG_FILE)

_USER_CONFIG = ConfigParser.ConfigParser()
_USER_CONFIG.read(USER_CONFIG_FILE)


def get_option(section, name):
    if _USER_CONFIG.has_option(section, name):
        return _USER_CONFIG.get(section, name)
    return _DEFAULT_CONFIG.get(section, name)


def _create_user_config():
    cf = open(USER_CONFIG_FILE, 'w')
    _DEFAULT_CONFIG.write(cf)
    cf.close()
    _USER_CONFIG.read(USER_CONFIG_FILE)


def open_user_config():
    if not path.isfile(USER_CONFIG_FILE):
        _create_user_config()
    system("start " + USER_CONFIG_FILE)
    exit()
