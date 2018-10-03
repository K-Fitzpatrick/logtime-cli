"""
Locate and manipulate logfiles.
"""

import os
import sys
import re
import string
from datetime import date, datetime
from logtime_cli.logtime_config import get_option

import logtime_cli.logfile_data as logfile_data

OUTPUT_TIME_FORMAT = '%I:%M %p'

def _format_entry(previous_time_entry, time_entry, task_entry, task_length):
    entry = "|\t" + str(previous_time_entry)
    entry += "\t|\t" + str(time_entry)
    entry += "\t|\t" + str(task_entry)
    entry += "\t|\t" + str(task_length)
    entry += "\t|\n"
    return entry


def _get_first_time_entry(entry_line):
    match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", entry_line)
    if match:
        return match[0]
    return None


def _get_second_time_entry(entry_line):
    match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", entry_line)
    if match:
        return match[1]
    return None


def _convert_time_of_day(time_of_day):
    if time_of_day == 'A' or time_of_day == 'a':
        return "AM"
    if time_of_day == 'P' or time_of_day == 'p':
        return "PM"
    return None


def _get_time_from_argument(arg_time):
    military_time_match = re.search('^([0-1][0-9]|[2][0-3]):?([0-6][0-9])$', arg_time)
    standard_time_match = re.search('^([0][0-9]|[1][0-2]):?([0-6][0-9])([AaPp])$', arg_time)

    time_match = military_time_match or standard_time_match
    if not time_match:
        raise ValueError('"' + arg_time + '" is not a valid time')

    hours = time_match.group(1)
    minutes = time_match.group(2)
    time_string = str(hours) + str(minutes)

    if military_time_match:
        output_date = datetime.strptime(time_string, "%H%M")
        return output_date.strftime(OUTPUT_TIME_FORMAT)
    elif standard_time_match:
        meridiem = standard_time_match.group(3)
        output_date = datetime.strptime(time_string + _convert_time_of_day(meridiem), "%I%M%p")
        return output_date.strftime(OUTPUT_TIME_FORMAT)
    return None


def _get_length_between_times(previous_time_entry, time_entry):
    from_date = datetime.strptime(previous_time_entry, OUTPUT_TIME_FORMAT)
    to_date = datetime.strptime(time_entry, OUTPUT_TIME_FORMAT)
    return (to_date - from_date).total_seconds() / 3600


def _update_length_between_times(file_path):
    logfile = open(file_path, "r")
    read_lines = logfile.readlines()
    logfile.close()
    logfile = open(file_path, "w")
    for current_line in read_lines:
        first_time_entry = _get_first_time_entry(current_line)
        if first_time_entry:
            second_time_entry = _get_second_time_entry(current_line)
            items = string.split(current_line, "|")
            length_between = _get_length_between_times(first_time_entry, second_time_entry)

            logfile.write(_format_entry(items[1].strip(), items[2].strip(), items[3].strip(),
                                        length_between))
        else:
            logfile.write(current_line)
    logfile.close()


def _create_new_log_file(file_path):
    logfile = open(file_path, "a+")
    logfile.write("# Notes:\n\n\n")
    logfile.write("# Time log:\n\n")
    logfile.write(_format_entry("Start", "End", "Task", "Length"))
    logfile.write(_format_entry("---", "---", "---", "---"))
    logfile.close()


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


def _print_last_line_to_console(file_path):
    logfile = open(file_path, "a+")
    lines = logfile.readlines()
    print lines[len(lines)-1]
    logfile.close()


def open_logfile_for_date(date_to_open, can_create=False):
    """
    Open the logfile for the given `date_to_open`.
    Will search the logfile directory as given in the configuration file
    for the file `YYYY-MM-DD.md`, as derived from the given `date_to_open`.
    If `can_create` is `True`, any unfound file will be created.
    """
    file_path = _get_file_path_for_date(date_to_open)

    if can_create and not os.path.isfile(file_path):
        _create_new_log_file(file_path)

    os.startfile(file_path)


def continue_last_entry():
    """
    Update the most recent time entry by setting the end time to the current time.
    """
    file_path = _get_file_path_for_date(date.today())

    if not os.path.isfile(file_path):
        _create_new_log_file(file_path)


    logfile = open(file_path, "r")
    lines = logfile.readlines()
    logfile.close()

    current_time_entry = datetime.today().time().strftime(OUTPUT_TIME_FORMAT)
    entry_line = lines[-1]
    time_regex = r"[0-1][0-9]:[0-6][0-9] [AP]M"

    match = re.findall(time_regex+r'.*'+time_regex, entry_line)
    if not entry_line or not match:
        raise ValueError('There is no time entry to continue.')

    new_entry_line = re.sub(r'('+time_regex+r'.*?)'+time_regex,
                            r'\g<1>'+current_time_entry, entry_line)

    logfile = open(file_path, "w")
    for current_line in lines[:-1]:
        logfile.write(current_line)
    logfile.write(new_entry_line)
    logfile.close()

    _update_length_between_times(file_path)
    _print_last_line_to_console(file_path)


def log_time(task_entry, start=None, end=None):
    """
    Log `task_entry` to today's logfile.
    Unless given, `start` will be defined as the last logged time.
    Unless given, `end` will be defined as the current time.
    """
    file_path = _get_file_path_for_date(date.today())

    if os.path.isfile(file_path):
        logfile_text = open(file_path).read()
        log_data = logfile_data.get_logfile(logfile_text)
    else:
        log_data = logfile_data.Logfile("", [])

    start_time = None
    if log_data.entries:
        start_time = log_data.entries[-1].end_time

    end_time = datetime.today().time()

    if start:
        start_time = start
    if end:
        end_time = end

    if start_time is None:
        start_time_str = get_option("DEFAULT", "new_day_start_time")
        start_time = datetime.strptime(start_time_str, OUTPUT_TIME_FORMAT).time()

    log_data.entries.append(logfile_data.Entry(start_time, end_time, task_entry))

    save_logfile(date.today(), log_data)
    _print_last_line_to_console(file_path)


def save_logfile(logfile_date, log_data):
    """Converts the given Logfile object to text, and saves it to a logfile at the given date"""
    file_path = _get_file_path_for_date(logfile_date)
    logfile_text = logfile_data.get_logfile_text(log_data)

    logfile = open(file_path, "w+")
    logfile.write(logfile_text)
    logfile.close()
