import os
import sys
import re
import string
from datetime import date, datetime, timedelta
from logtime_cli.logtime_config import GetOption

OUTPUT_TIME_FORMAT = '%I:%M %p'

def _format_entry(previous_time_entry, time_entry, task_entry, task_length):
    return "|\t" + str(previous_time_entry) + "\t|\t" + str(time_entry) + "\t|\t" + str(task_entry) + "\t|\t" + str(task_length) + "\t|\n"


def _get_first_time_entry(entry_line):
    match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", entry_line)
    if match:
        return match[0]
    else:
        return None


def _get_second_time_entry(entry_line):
    match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", entry_line)
    if match:
        return match[1]
    else:
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
    if not (time_match):
        raise ValueError('"' + arg_time + '" is not a valid time')

    hours = time_match.group(1)
    minutes = time_match.group(2)
    time_string = str(hours) + str(minutes)

    if military_time_match:
        return datetime.strptime(time_string, "%H%M").strftime(OUTPUT_TIME_FORMAT)
    elif standard_time_match:
        meridiem = standard_time_match.group(3)
        return datetime.strptime(time_string + _convert_time_of_day(meridiem), "%I%M%p").strftime(OUTPUT_TIME_FORMAT)


def _get_length_between_times(previous_time_entry, time_entry):
    d1 = datetime.strptime(previous_time_entry, OUTPUT_TIME_FORMAT)
    d2 = datetime.strptime(time_entry, OUTPUT_TIME_FORMAT)
    return (d2 - d1).total_seconds() / 3600


def _update_length_between_times(file_path):
    f = open(file_path, "r")
    read_lines = f.readlines()
    f.close()
    f = open(file_path, "w")
    for current_line in read_lines:
        first_time_entry = _get_first_time_entry(current_line)
        if first_time_entry:
            second_time_entry = _get_second_time_entry(current_line)
            items = string.split(current_line, "|")
            f.write(_format_entry(items[1].strip(), items[2].strip(), items[3].strip(), _get_length_between_times(first_time_entry, second_time_entry)))
        else:
            f.write(current_line)
    f.close()


def _create_new_log_file(file_path):
    f = open(file_path, "a+")
    f.write("# Notes:\n\n\n")
    f.write("# Time log:\n\n")
    f.write(_format_entry("Start", "End", "Task", "Length"))
    f.write(_format_entry("---", "---", "---", "---"))
    f.close()


def _get_log_file_directory():
    log_file_directory = GetOption('DEFAULT', 'logfile_directory')
    if not os.path.exists(log_file_directory):
        os.mkdir(log_file_directory)
    return log_file_directory


def _get_file_path_for_date(date):
    #Always reset path to this file
    if os.path.isdir(sys.path[0]):
        os.chdir(sys.path[0])
    else:
        os.chdir(os.path.dirname(sys.path[0]))

    log_file_directory = _get_log_file_directory()

    current_date = date.isoformat()
    file_path = os.path.join(log_file_directory, current_date + ".md")

    return os.path.abspath(file_path)


def _print_last_line_to_console(file_path):
    f = open(file_path, "a+")
    lines = f.readlines()
    print lines[len(lines)-1]
    f.close()


def open_logfile_for_date(date_to_open, can_create=False):
    file_path = _get_file_path_for_date(date_to_open)

    if can_create and not os.path.isfile(file_path):
        _create_new_log_file(file_path)

    os.startfile(file_path)


def log_time(task_entry, start, end):
    file_path = _get_file_path_for_date(date.today())

    if not os.path.isfile(file_path):
        _create_new_log_file(file_path)

    _update_length_between_times(file_path)

    f = open(file_path, "a+")
    lines = f.readlines()
    last_time_entry = _get_second_time_entry(lines[len(lines)-1])
    current_time_entry = datetime.today().time().strftime(OUTPUT_TIME_FORMAT)

    if start:
        last_time_entry = _get_time_from_argument(start)
    if end:
        current_time_entry = _get_time_from_argument(end)

    if last_time_entry:
        f.write(_format_entry(last_time_entry, current_time_entry, task_entry, _get_length_between_times(last_time_entry, current_time_entry)))
    else:
        start_time = GetOption("DEFAULT", "new_day_start_time")
        f.write(_format_entry(start_time, current_time_entry, task_entry, _get_length_between_times(start_time, current_time_entry)))
    f.close()

    _print_last_line_to_console(file_path)
