[![PyPI](https://img.shields.io/pypi/v/logtime-cli.svg)](https://pypi.python.org/pypi/logtime-cli)

## logtime.py

Simple CLI time logging application.

Meant to track what you just finished working on, and deliver readable text output.

## Installation
```bash
pip install logtime-cli
```

## Usage
To log time:
```
lt what I just finished doing
```

To open your daily log file:
```
lt
```
To open yesterday's daily log file:
```
lt -p
```

To log time with an end date:
```
lt 07:15a what I did during that time
lt 12:15p what I did during that time
```

To log time with a start and end date:
```
lt 07:15a 07:30a what I did during that time
```

## Configuration
In your installation directory (with pip, `C:\<PATH_TO_PYTHON>\Lib\site-packages\logtime-cli`), you'll find a file `config/config-default.ini`.

Copy that file to `config/config-user.ini`, and change that file as needed.

- **`new_day_start_time`** affects what time each day is assumed to start at for the first call of `lt something`. Example: `10:00 AM`
- **`logfile_directory`** is where the logtime files get stored. Works on relative and absolute paths. Example: `C:\...\Dropbox\logtime-logs`
