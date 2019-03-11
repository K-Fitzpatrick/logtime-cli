"""
Responsibilities:
    Represent logfile data
    Convert to/from object representation
"""

from datetime import date, datetime
import string
import re
from collections import namedtuple
import logtime_cli.logfile_notes_data as logfile_notes_data

OUTPUT_TIME_FORMAT = "%I:%M %p"

# Models
Logfile = namedtuple('Logfile', ['notes', 'entries'])

def get_notes_data(log_data):
    """Return the logfile notes data of a Logfile data object.

    Assumes the primary Notes section title, as that knowledge belongs in this file.
    """
    return logfile_notes_data.LogfileNotesSection(name='Notes:', full_text=log_data.notes)

def _strip_seconds(current_time):
    return datetime.combine(date.min, current_time).replace(second=0, microsecond=0).time()

class Entry(object):
    """A single time period logged in a logfile"""
    def __init__(self, start_time, end_time, task):
        self.__start_time = None
        self.__end_time = None

        self.start_time = start_time
        self.end_time = end_time
        self.task = task

    def __eq__(self, comp):
        return (
            self.start_time == comp.start_time
            and self.end_time == comp.end_time
            and self.task == comp.task
        )

    def __ne__(self, comp):
        return not self.__eq__(comp)

    @property
    def start_time(self):
        """The start time, down to the minute"""
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        self.__start_time = _strip_seconds(value) if value is not None else None

    @property
    def end_time(self):
        """The end time, down to the minute"""
        return self.__end_time

    @end_time.setter
    def end_time(self, value):
        self.__end_time = _strip_seconds(value) if value is not None else None

    def duration(self):
        """Return duration of the Entry in seconds"""
        delta = (datetime.combine(date.min, self.end_time)
                 - datetime.combine(date.min, self.start_time))
        return delta.total_seconds() / 3600


def _get_notes_text(logfile_text):
    match = re.findall("# Notes:\n(.*?)\n\n# Time log:", logfile_text, re.DOTALL)
    if match:
        return match[0]
    return None


def _get_timelog_section(logfile_text):
    match = re.findall("# Time log:.*", logfile_text, re.DOTALL)
    if match:
        return match[0]
    return None


def _get_timelog_entries(logfile_text):
    timelog_section = _get_timelog_section(logfile_text)
    entries = []

    for current_line in timelog_section.splitlines():
        match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", current_line)
        if match:
            items = [item.strip() for item in string.split(current_line, '|')]
            entry = Entry(
                start_time=datetime.strptime(items[1], OUTPUT_TIME_FORMAT).time(),
                end_time=datetime.strptime(items[2], OUTPUT_TIME_FORMAT).time(),
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
    return _format_entry(
        entry.start_time.strftime(OUTPUT_TIME_FORMAT),
        entry.end_time.strftime(OUTPUT_TIME_FORMAT),
        entry.task,
        entry.duration(),
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
