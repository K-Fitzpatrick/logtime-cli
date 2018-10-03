import unittest
from datetime import datetime
from logtime_cli.logfile_data.markdown_dal import _get_logfile, _get_logfile_text, Entry, Logfile

test_text = '\n'.join([
    "# Notes:",
    "meow",
    "meow",
    "meow",
    "meow",
    "",
    "# Time log:",
    "",
    "|\tStart\t|\tEnd\t|\tTask\t|\tLength\t|",
    "|\t---\t|\t---\t|\t---\t|\t---\t|",
    "|\t11:45 AM\t|\t12:05 PM\t|\tlogtime: pie charts\t|\t0.333333333333\t|",
    "|\t12:05 PM\t|\t12:17 PM\t|\tlogtime: requirements\t|\t0.2\t|",
    "|\t12:17 PM\t|\t02:00 PM\t|\tlogtime: refactor design\t|\t1.71666666667\t|",
    "|\t02:00 PM\t|\t02:15 PM\t|\tid verification form\t|\t0.25\t|",
    "|\t02:15 PM\t|\t02:44 PM\t|\tlogtime: logtime parser\t|\t0.483333333333\t|",
    "|\t02:44 PM\t|\t04:10 PM\t|\tlogtime: pie charts\t|\t1.43333333333\t|",
    "",
])

test_logfile = Logfile(
    notes="meow\nmeow\nmeow\nmeow",
    entries=[
        Entry(start_time=datetime.strptime("11:45 AM", "%I:%M %p"), end_time=datetime.strptime("12:05 PM", "%I:%M %p"), task="logtime: pie charts"),
        Entry(start_time=datetime.strptime("12:05 PM", "%I:%M %p"), end_time=datetime.strptime("12:17 PM", "%I:%M %p"), task="logtime: requirements"),
        Entry(start_time=datetime.strptime("12:17 PM", "%I:%M %p"), end_time=datetime.strptime("02:00 PM", "%I:%M %p"), task="logtime: refactor design"),
        Entry(start_time=datetime.strptime("02:00 PM", "%I:%M %p"), end_time=datetime.strptime("02:15 PM", "%I:%M %p"), task="id verification form"),
        Entry(start_time=datetime.strptime("02:15 PM", "%I:%M %p"), end_time=datetime.strptime("02:44 PM", "%I:%M %p"), task="logtime: logtime parser"),
        Entry(start_time=datetime.strptime("02:44 PM", "%I:%M %p"), end_time=datetime.strptime("04:10 PM", "%I:%M %p"), task="logtime: pie charts"),
    ],
)


class Test_Load(unittest.TestCase):
    def test_markdown_to_logfile_conversion(self):
        logfile = _get_logfile(test_text)

        self.assertEqual(logfile.notes, test_logfile.notes)
        self.assertEqual(logfile.entries, test_logfile.entries)


class Test_Save(unittest.TestCase):
    def test_logfile_to_markdown_conversion(self):
        logfile_text = _get_logfile_text(test_logfile)

        self.assertEqual(logfile_text, test_text)


if __name__ == '__main__':
    unittest.main()
