'''
"Database" handling
'''

from datetime import date, datetime
import os
import sys
import string
import re
from logtime_cli.logtime_config import get_option
from collections import namedtuple

OUTPUT_TIME_FORMAT = '%I:%M %p'

# Models
Entry = namedtuple('Entry', ['start_time', 'end_time', 'task'])
Logfile = namedtuple('Logfile', ['notes', 'entries'])


def _get_log_file_directory():
    log_file_directory = get_option('DEFAULT', 'logfile_directory')
    if not os.path.exists(log_file_directory):
        os.mkdir(log_file_directory)
    return log_file_directory


def _get_file_path_for_date(date_for_file_name):
    #Always reset path to this file
    if os.path.isdir(sys.path[0]):
        os.chdir(sys.path[0])
    else:
        os.chdir(os.path.dirname(sys.path[0]))

    log_file_directory = _get_log_file_directory()

    current_date = date_for_file_name.isoformat()
    file_path = os.path.join(log_file_directory, current_date + ".md")

    return os.path.abspath(file_path)


def _get_notes_text(logfile_text):
    match = re.findall("# Notes:\n(.*?)\n\n# Time log:", logfile_text, re.DOTALL)
    if match:
        return match[0]


def _get_timelog_section(logfile_text):
    match = re.findall("# Time log:.*", logfile_text, re.DOTALL)
    if match:
        return match[0]


def _get_timelog_entries(logfile_text):
    timelog_section = _get_timelog_section(logfile_text)
    entries = []

    for current_line in timelog_section.splitlines():
        match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", current_line)
        if match:
            items = [item.strip() for item in string.split(current_line, '|')]
            entry = Entry(
                start_time=datetime.strptime(items[1], "%I:%M %p"),
                end_time=datetime.strptime(items[2], "%I:%M %p"),
                task=items[3],
            )
            entries.append(entry)
    return entries


def _get_logfile(logfile_text):
    notes_text = _get_notes_text(logfile_text)
    timelog_entries = _get_timelog_entries(logfile_text)

    logfile = Logfile(
        notes=notes_text,
        entries=timelog_entries,
    )

    return logfile


def _format_entry(previous_time_entry, time_entry, task_entry, task_length):
    entry = "|\t" + str(previous_time_entry)
    entry += "\t|\t" + str(time_entry)
    entry += "\t|\t" + str(task_entry)
    entry += "\t|\t" + str(task_length)
    entry += "\t|\n"
    return entry


def _get_logfile_text(logfile):
    logfile_text = "# Notes:\n"
    logfile_text += logfile.notes + "\n"
    logfile_text += "\n"
    logfile_text += ("# Time log:\n\n")
    logfile_text += (_format_entry("Start", "End", "Task", "Length"))
    logfile_text += (_format_entry("---", "---", "---", "---"))
    for entry in logfile.entries:
        logfile_text += _format_entry(
            entry.start_time.strftime(OUTPUT_TIME_FORMAT),
            entry.end_time.strftime(OUTPUT_TIME_FORMAT),
            entry.task,
            (entry.end_time - entry.start_time).total_seconds() / 3600,
        )

    return logfile_text


def load_logfile(logfile_date):
    """Opens the logfile at the given date, and returns a Logfile object"""
    file_path = _get_file_path_for_date(logfile_date)
    logfile_text = open(file_path).read()
    return _get_logfile(logfile_text)


def save_logfile(logfile_date, logfile):
    """Converts the given Logfile object to text, and saves it to a logfile at the given date"""
    file_path = _get_file_path_for_date(logfile_date)
    logfile_text = _get_logfile_text(logfile)

    logfile = open(file_path, "a+")
    logfile.write(logfile_text)
    logfile.close()
