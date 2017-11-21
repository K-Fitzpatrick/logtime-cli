'''
Calculate and display a pie-chart of the day's logged time.
'''

import re
import string
from matplotlib import pyplot
from collections import defaultdict, namedtuple
from datetime import datetime, timedelta


def _get_task_times(entries):
    task_times = defaultdict(lambda: timedelta())
    for entry in entries:
        time_diff = entry.end_time - entry.start_time
        task_times[entry.task] += time_diff
    return task_times


def _get_timelog_entries(logfile_text):
    Entry = namedtuple('Entry', ['start_time', 'end_time', 'task'])
    entries = []
    for current_line in logfile_text:
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


def _make_autopct(task_durations):
    def autopct(curr_pct):
        total_seconds = sum(task_durations)
        curr_seconds = int(round(curr_pct*total_seconds/100.0))

        hours = curr_seconds / (60*60)
        remaining_minutes = (curr_seconds % (60*60)) / 60

        return '{p:.2f}% \n ({h:.0f}h:{m:.0f}m)'.format(p=curr_pct, h=hours, m=remaining_minutes)
    return autopct


def show_pie(logfile_text, date):
    """
    Display a pie chart of the day's logged time given a logfile in the form of `logfile_text`.
    `date` is currently only for the graph's title.
    """
    entries = _get_timelog_entries(logfile_text)
    task_times = _get_task_times(entries)

    task_durations = [task_times[task].total_seconds() for task in task_times]

    pyplot.pie(
        x=task_durations,
        labels=[task for task in task_times],
        autopct=_make_autopct(task_durations),
    )

    seconds = sum(task_durations)
    hours = int(seconds / (60*60))
    remaining_minutes = (seconds % (60*60)) / 60

    title = date.isoformat()+'\n'
    title += 'Total time: {h:.0f}h:{m:.0f}m'.format(h=hours, m=remaining_minutes)
    pyplot.title(title)

    pyplot.show()
