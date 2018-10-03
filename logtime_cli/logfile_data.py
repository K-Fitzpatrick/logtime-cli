'''
"Database" handling
'''

from datetime import date, datetime
import string
import re
from collections import namedtuple

OUTPUT_TIME_FORMAT = '%I:%M %p'

# Models
Entry = namedtuple('Entry', ['start_time', 'end_time', 'task'])
Logfile = namedtuple('Logfile', ['notes', 'entries'])


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
                start_time=datetime.strptime(items[1], "%I:%M %p").time(),
                end_time=datetime.strptime(items[2], "%I:%M %p").time(),
                task=items[3],
            )
            entries.append(entry)
    return entries


def get_logfile(logfile_text):
    """Given the text of a logfile, return its component parts as a Logfile object"""
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

def format_entry(entry):
    """Converts an Entry into a markdown table entry, and returns it as a string"""
    start_datetime = datetime.combine(date.today(), entry.start_time).replace(second=0, microsecond=0)
    end_datetime = datetime.combine(date.today(), entry.end_time).replace(second=0, microsecond=0)

    return _format_entry(
        entry.start_time.strftime(OUTPUT_TIME_FORMAT),
        entry.end_time.strftime(OUTPUT_TIME_FORMAT),
        entry.task,
        (end_datetime - start_datetime).total_seconds() / 3600,
    )

def get_logfile_text(logfile):
    """Converts the given Logfile object to formatted text, and returns it as a giant string"""
    logfile_text = "# Notes:\n"
    logfile_text += logfile.notes + "\n"
    logfile_text += "\n"
    logfile_text += ("# Time log:\n\n")
    logfile_text += (_format_entry("Start", "End", "Task", "Length"))
    logfile_text += (_format_entry("---", "---", "---", "---"))
    for entry in logfile.entries:
        logfile_text += format_entry(entry)

    return logfile_text
