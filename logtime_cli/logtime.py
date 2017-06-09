import os
import sys
import re
import string
from datetime import date, datetime, timedelta
from logtime_cli.logtime_config import GetOption

OUTPUT_TIME_FORMAT = '%I:%M %p'

def _formatEntry(previousTimeEntry, timeEntry, taskEntry, taskLength):
    return "|\t" + str(previousTimeEntry) + "\t|\t" + str(timeEntry) + "\t|\t" + str(taskEntry) + "\t|\t" + str(taskLength) + "\t|\n"


def _getFirstTimeEntry(entryLine):
    match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", entryLine)
    if match:
        return match[0]
    else:
        return None


def _getSecondTimeEntry(entryLine):
    match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", entryLine)
    if match:
        return match[1]
    else:
        return None


def _convertTimeOfDay(timeOfDay):
    if timeOfDay == 'A' or timeOfDay == 'a':
        return "AM"
    if timeOfDay == 'P' or timeOfDay == 'p':
        return "PM"
    return None


def _getTimeFromArgument(argTime):
    military_time_match = re.search('^([0-1][0-9]|[2][0-3]):?([0-6][0-9])$', argTime)
    standard_time_match = re.search('^([0][0-9]|[1][0-2]):?([0-6][0-9])([AaPp])$', argTime)

    time_match = military_time_match or standard_time_match
    if not (time_match):
        raise ValueError('"' + argTime + '" is not a valid time')

    hours = time_match.group(1)
    minutes = time_match.group(2)
    timeString = str(hours) + str(minutes)

    if military_time_match:
        return datetime.strptime(timeString, "%H%M").strftime(OUTPUT_TIME_FORMAT)
    elif standard_time_match:
        meridiem = standard_time_match.group(3)
        return datetime.strptime(timeString + _convertTimeOfDay(meridiem), "%I%M%p").strftime(OUTPUT_TIME_FORMAT)


def _getLengthBetweenTimes(previousTimeEntry, timeEntry):
    d1 = datetime.strptime(previousTimeEntry, OUTPUT_TIME_FORMAT)
    d2 = datetime.strptime(timeEntry, OUTPUT_TIME_FORMAT)
    return (d2 - d1).total_seconds() / 3600


def _updateLengthBetweenTimes(filePath):
    f = open(filePath, "r")
    readLines = f.readlines()
    f.close()
    f = open(filePath, "w")
    for currentLine in readLines:
        firstTimeEntry = _getFirstTimeEntry(currentLine)
        if firstTimeEntry:
            secondTimeEntry = _getSecondTimeEntry(currentLine)
            items = string.split(currentLine, "|")
            f.write(_formatEntry(items[1].strip(), items[2].strip(), items[3].strip(), _getLengthBetweenTimes(firstTimeEntry, secondTimeEntry)))
        else:
            f.write(currentLine)
    f.close()


def _getFilePathForDate(date):
    #Always reset path to this file
    if os.path.isdir(sys.path[0]):
        os.chdir(sys.path[0])
    else:
        os.chdir(os.path.dirname(sys.path[0]))

    logFileDirectory = GetOption('DEFAULT', 'logfile_directory')

    if not os.path.exists(logFileDirectory):
        os.mkdir(logFileDirectory)

    currentDate = date.isoformat()
    filePath = logFileDirectory + "/" + currentDate + ".md"

    if not os.path.isfile(filePath):
        f = open(filePath, "a+")
        f.write("# Notes:\n\n\n")
        f.write("# Time log:\n\n")
        f.write(_formatEntry("Start", "End", "Task", "Length"))
        f.write(_formatEntry("---", "---", "---", "---"))
        f.close()

    return os.path.abspath(filePath)


def _printLastLineToConsole(filePath):
    f = open(filePath, "a+")
    lines = f.readlines()
    print lines[len(lines)-1]
    f.close()


def OpenLogfileForDate(dateToOpen):
    os.startfile(_getFilePathForDate(dateToOpen))


def LogTime(taskEntry, start, end):
    filePath = _getFilePathForDate(date.today())

    _updateLengthBetweenTimes(filePath)

    f = open(filePath, "a+")
    lines = f.readlines()
    lastTimeEntry = _getSecondTimeEntry(lines[len(lines)-1])
    currentTimeEntry = datetime.today().time().strftime(OUTPUT_TIME_FORMAT)

    if start:
        lastTimeEntry = _getTimeFromArgument(start)
    if end:
        currentTimeEntry = _getTimeFromArgument(end)

    if lastTimeEntry:
        f.write(_formatEntry(lastTimeEntry, currentTimeEntry, taskEntry, _getLengthBetweenTimes(lastTimeEntry, currentTimeEntry)))
    else:
        startTime = GetOption("DEFAULT", "new_day_start_time")
        f.write(_formatEntry(startTime, currentTimeEntry, taskEntry, _getLengthBetweenTimes(startTime, currentTimeEntry)))
    f.close()

    _printLastLineToConsole(filePath)
