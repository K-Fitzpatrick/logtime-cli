#!/usr/bin/env python


# Usage
#
# 1. Put this file on your path.
# 1. Add `alias lt="logtime.py` to your `bash.bashrc` file
#
# To log time: Type `lt "thing"` into your bash shell
# To open your daily log file:  type or `lt`


import os
import sys
import re
from datetime import date, datetime

def _formatEntry(previousTimeEntry, timeEntry, taskEntry):
   return "|\t"  + str(previousTimeEntry) + "\t|\t" + str(timeEntry) + "\t|\t" + str(taskEntry) + "\t|\n"

def _getTimeEntry(entryLine):
   match = re.findall("([0-1][0-9]:[0-6][0-9] [AP]M)", lines[len(lines)-1])
   if match:
      return match[1]
   else:
      return None


#Always reset path to this file
if os.path.isdir(sys.path[0]):
   os.chdir(sys.path[0])
else:
   os.chdir(os.path.dirname(sys.path[0]))

logFileDirectory = "time-log-files"

if not os.path.exists(logFileDirectory):
   os.mkdir(logFileDirectory)

currentDate = date.today().isoformat()
filePath = logFileDirectory + "/" + currentDate + ".md"

currentTimeEntry = datetime.today().time().strftime("%I:%M %p")
taskEntry = " ".join(sys.argv[1:])

if not os.path.isfile(filePath):
   f = open(filePath, "a+")
   f.write("# Notes:\n\n\n\n")
   f.write("# Time log:\n\n")
   f.write(_formatEntry("Start", "End", "Task"))
   f.write(_formatEntry("---", "---", "---"))
   f.close()

if len(sys.argv) < 2:
   os.system("start " + filePath)
else:
   f = open(filePath, "a+")
   lines = f.readlines()

   lastTimeEntry = _getTimeEntry(lines[len(lines)-1])
   if lastTimeEntry:
      f.write(_formatEntry(lastTimeEntry, currentTimeEntry, taskEntry))
   else:
      f.write(_formatEntry("09:00 AM", currentTimeEntry, taskEntry))

   f = open(filePath, "a+")
   lines = f.readlines()
   print lines[len(lines)-1]

   f.close()
