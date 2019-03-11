'''
Calculate and display a pie-chart of the day's logged time.
'''

from collections import defaultdict
from datetime import date, datetime, timedelta
from matplotlib import pyplot

import logtime_cli.logfile_data as logfile_data

def _get_task_times(entries):
    task_times = defaultdict(lambda: timedelta())
    for entry in entries:
        start_datetime = datetime.combine(date.today(), entry.start_time).replace(second=0, microsecond=0)
        end_datetime = datetime.combine(date.today(), entry.end_time).replace(second=0, microsecond=0)

        time_diff = end_datetime - start_datetime
        task_times[entry.task] += time_diff
    return task_times


def _make_autopct(task_durations):
    def _autopct(curr_pct):
        total_seconds = sum(task_durations)
        curr_seconds = int(round(curr_pct*total_seconds/100.0))

        hours = curr_seconds / (60*60)
        remaining_minutes = (curr_seconds % (60*60)) / 60

        return '{p:.2f}% \n ({h:.0f}h:{m:.0f}m)'.format(p=curr_pct, h=hours, m=remaining_minutes)
    return _autopct


def show_pie(log_data, title_date):
    """
    Display a pie chart of the day's logged time given a logfile object.
    `title_date` is currently only for the graph's title.
    """
    task_times = _get_task_times(log_data.entries)

    task_durations = [task_times[task].total_seconds() for task in task_times]

    pyplot.pie(
        x=task_durations,
        labels=[task for task in task_times],
        autopct=_make_autopct(task_durations),
    )

    seconds = sum(task_durations)
    hours = int(seconds / (60*60))
    remaining_minutes = (seconds % (60*60)) / 60

    title = title_date.isoformat()+'\n'
    title += 'Total time: {h:.0f}h:{m:.0f}m'.format(h=hours, m=remaining_minutes)
    pyplot.title(title)

    pyplot.show()
