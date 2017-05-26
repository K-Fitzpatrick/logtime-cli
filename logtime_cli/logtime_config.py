import ConfigParser
from os import path, system

DEFAULT_CONFIG_FILE = path.dirname(__file__) + '/config/config-default.ini'
USER_CONFIG_FILE = path.dirname(__file__) + '/config/config-user.ini'

_defaultConfig = ConfigParser.ConfigParser()
_defaultConfig.read(DEFAULT_CONFIG_FILE)

_userConfig = ConfigParser.ConfigParser()
_userConfig.read(USER_CONFIG_FILE)


def GetOption(section, name):
    if _userConfig.has_option(section, name):
        return _userConfig.get(section, name)
    return _defaultConfig.get(section, name)


def _createUserConfig():
    cf = open(USER_CONFIG_FILE, 'w')
    _defaultConfig.write(cf)
    cf.close()
    _userConfig.read(USER_CONFIG_FILE)


def OpenUserConfig():
    if not path.isfile(USER_CONFIG_FILE):
        _createUserConfig()
    system("start " + USER_CONFIG_FILE)
    exit()
