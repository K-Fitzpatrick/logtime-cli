import unittest
from datetime import datetime
import logtime_cli.logfile_data as logfile_data

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
    "|\t11:45 AM\t|\t12:05 PM\t|\tlogtime: pie charts\t|\t0.3333333333333333\t|",
    "|\t12:05 PM\t|\t12:17 PM\t|\tlogtime: requirements\t|\t0.2\t|",
    "|\t12:17 PM\t|\t02:00 PM\t|\tlogtime: refactor design\t|\t1.7166666666666666\t|",
    "|\t02:00 PM\t|\t02:15 PM\t|\tid verification form\t|\t0.25\t|",
    "|\t02:15 PM\t|\t02:44 PM\t|\tlogtime: logtime parser\t|\t0.48333333333333334\t|",
    "|\t02:44 PM\t|\t04:10 PM\t|\tlogtime: pie charts\t|\t1.4333333333333333\t|",
    "",
])

test_logfile = logfile_data.Logfile(
    notes="meow\nmeow\nmeow\nmeow",
    entries=[
        logfile_data.Entry(start_time=datetime.strptime("11:45 AM", "%I:%M %p").time(), end_time=datetime.strptime("12:05 PM", "%I:%M %p").time(), task="logtime: pie charts"),
        logfile_data.Entry(start_time=datetime.strptime("12:05 PM", "%I:%M %p").time(), end_time=datetime.strptime("12:17 PM", "%I:%M %p").time(), task="logtime: requirements"),
        logfile_data.Entry(start_time=datetime.strptime("12:17 PM", "%I:%M %p").time(), end_time=datetime.strptime("02:00 PM", "%I:%M %p").time(), task="logtime: refactor design"),
        logfile_data.Entry(start_time=datetime.strptime("02:00 PM", "%I:%M %p").time(), end_time=datetime.strptime("02:15 PM", "%I:%M %p").time(), task="id verification form"),
        logfile_data.Entry(start_time=datetime.strptime("02:15 PM", "%I:%M %p").time(), end_time=datetime.strptime("02:44 PM", "%I:%M %p").time(), task="logtime: logtime parser"),
        logfile_data.Entry(start_time=datetime.strptime("02:44 PM", "%I:%M %p").time(), end_time=datetime.strptime("04:10 PM", "%I:%M %p").time(), task="logtime: pie charts"),
    ],
)


class Test_Load(unittest.TestCase):
    def test_markdown_to_logfile_conversion(self):
        logfile = logfile_data.get_logfile(test_text)

        self.assertEqual(logfile.notes, test_logfile.notes)
        self.assertEqual(logfile.entries, test_logfile.entries)


class Test_Save(unittest.TestCase):
    def test_logfile_to_markdown_conversion(self):
        logfile_text = logfile_data.get_logfile_text(test_logfile)

        self.assertEqual(logfile_text, test_text)


if __name__ == '__main__':
    unittest.main()
