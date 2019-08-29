"""
Locate and manipulate logfiles.
"""
from __future__ import print_function

from datetime import date, datetime
from logtime_cli.logtime_config import get_option

import logtime_cli.logfile_io as logfile_io
import logtime_cli.logfile_data as logfile_data

NEW_DAY_START_TIME_FORMAT = '%I:%M %p'


def open_logfile_for_date(date_to_open, can_create=False):
    """
    Open the logfile for the given `date_to_open`.
    Will search the logfile directory as given in the configuration file
    for the file `YYYY-MM-DD.md`, as derived from the given `date_to_open`.
    If `can_create` is `True`, any unfound file will be created.
    """
    if can_create and not logfile_io.exists(date_to_open):
        log_data = logfile_data.Logfile("", [])
        logfile_io.save_logfile(date_to_open, log_data)

    logfile_io.open_file_in_editor(date_to_open)


def continue_last_entry():
    """
    Update the most recent time entry by setting the end time to the current time.
    """
    logfile_date = date.today()

    if logfile_io.exists(logfile_date):
        log_data = logfile_io.load_logfile(logfile_date)
    else:
        log_data = logfile_data.Logfile("", [])
        logfile_io.save_logfile(logfile_date, log_data)

    if not log_data.entries:
        raise ValueError('There is no time entry to continue.')

    current_time = datetime.today().time()
    log_data.entries[-1].end_time = current_time

    logfile_io.save_logfile(logfile_date, log_data)
    print(logfile_io.get_last_entry_line(logfile_date))


def recalculate():
    """
    Recalulate each of the days time entries
    """
    logfile_date = date.today()

    if not logfile_io.exists(logfile_date):
        raise ValueError('There is no time entry to recalculate')

    log_data = logfile_io.load_logfile(logfile_date)

    if not log_data.entries:
        raise ValueError('There is no time entry to recalculate')

    logfile_io.save_logfile(logfile_date, log_data)
    print('Recalulated')


def log_time(task_entry, start=None, end=None):
    """
    Log `task_entry` to today's logfile.
    Unless given, `start` will be defined as the last logged time.
    Unless given, `end` will be defined as the current time.
    """
    logfile_date = date.today()

    if logfile_io.exists(logfile_date):
        log_data = logfile_io.load_logfile(logfile_date)
    else:
        log_data = logfile_data.Logfile("", [])

    if start is not None:
        start_time = start
    elif log_data.entries:
        start_time = log_data.entries[-1].end_time
    else:
        start_time_str = get_option("DEFAULT", "new_day_start_time")
        start_time = datetime.strptime(start_time_str, NEW_DAY_START_TIME_FORMAT).time()

    if end is not None:
        end_time = end
    else:
        end_time = datetime.today().time()

    log_data.entries.append(logfile_data.Entry(start_time, end_time, task_entry))

    logfile_io.save_logfile(date.today(), log_data)
    print(logfile_io.get_last_entry_line(logfile_date))
