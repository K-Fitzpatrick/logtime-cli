"""
Responsibilities:
    Manipulate logfile I/O
"""

import os
import sys
from io import open
import logtime_cli.logfile_data as logfile_data
import logtime_cli.logtime_config as logtime_config

def _get_log_file_directory():
    log_file_directory = logtime_config.get_option('DEFAULT', 'logfile_directory')
    if not os.path.exists(log_file_directory):
        os.mkdir(log_file_directory)
    return log_file_directory

def open_file_in_editor(logfile_date):
    """Asks operating system to open this file using the default editor"""
    file_path = get_file_path_for_date(logfile_date)
    os.startfile(file_path)

def get_last_entry_line(logfile_date):
    """Returns the last entry line of the logfile, formatted as-is"""
    file_path = get_file_path_for_date(logfile_date)

    logfile = open(file_path, "a+", encoding='utf-8')
    logfile.seek(0)
    lines = logfile.readlines()
    logfile.close()

    return lines[len(lines)-1]


def get_file_path_for_date(logfile_date):
    """Given a date, returns the full file path for the logfile for that date"""
    #Always reset path to this file
    if os.path.isdir(sys.path[0]):
        os.chdir(sys.path[0])
    else:
        os.chdir(os.path.dirname(sys.path[0]))

    log_file_directory = _get_log_file_directory()

    current_date = logfile_date.isoformat()
    file_path = os.path.join(log_file_directory, current_date + ".md")

    return os.path.abspath(file_path)

def exists(logfile_date):
    """Returns true if a logfile exists for the given date"""
    file_path = get_file_path_for_date(logfile_date)
    return os.path.isfile(file_path)

def load_logfile(logfile_date):
    """Opens the logfile at the given date, and returns a Logfile object"""
    file_path = get_file_path_for_date(logfile_date)
    logfile_text = open(file_path, encoding='utf-8').read()
    return logfile_data.get_logfile(logfile_text)


def save_logfile(logfile_date, log_data):
    """Converts the given Logfile object to text, and saves it to a logfile at the given date"""
    file_path = get_file_path_for_date(logfile_date)
    logfile_text = logfile_data.get_logfile_text(log_data)

    logfile = open(file_path, "w+", encoding='utf-8')
    logfile.write(logfile_text)
    logfile.close()
