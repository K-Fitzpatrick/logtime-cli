[![PyPI](https://img.shields.io/pypi/v/logtime-cli.svg)](https://pypi.python.org/pypi/logtime-cli)

## logtime.py

Simple CLI time logging application.

Meant to track what you just finished working on, and deliver readable text output.

## Installation
```bash
pip install logtime-cli
```

## Tests
To run tests, `pip install nose` and run

```
nosetests
```

## Help
```
lt --help
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
To open a previous daily log file:
```
lt -p
lt -p 2 //opens daily log from 2 days ago
```

To log time with an end date:
```
lt -e 07:15p what I did during that time
lt -e 19:15 what I did during that time
lt -e 0715p what I did during that time
lt -e 1915 what I did during that time
```

To log time with a start and end date:
```
lt -s 07:15a -e 07:30a what I did during that time
```

## Example workflows
```
lt what I just finished doing
```
```
lt -s 0700 what I just finished doing, when this is the first thing I logged today
```
```
lt -e 1100 what I know I stopped doing at 1100, but forgot to log
lt what I just finished doing
```
```
lt -b what I am about to do, when this is the first thing I logged in a while
# ... later, when I'm done ...
lt -c
```

## Additional options
- `--pie` will display a pie chart of today's time log

## Reporting options
The `logtime` command group helps gather data.

- Display today's worked hours. (`logtime calc -h`)
- Count the number of tasks on a given day (`logtime count_tasks -h`)
- Display all logfiles (useful for using `lt -p` to open logfiles) (`logtime list -h`)
- Print the `## Summary` section from every day of this week (`logtime summarize_week -h`)
    - *`logtime summarize_week | clip` is very useful*
- Print all sections of a given name throughout your entire log history (`logtime section_report -h`)
    - *`logtime section_report "Summary" | less`*

## Configuration
```
lt --config
```

- **`new_day_start_time`** affects what time each day is assumed to start at for the first call of `lt something`. Example: `10:00 AM`
- **`logfile_directory`** is where the logtime files get stored. Works on relative and absolute paths. Example: `C:\...\Dropbox\logtime-logs`

### Manually find config
In your installation directory (with pip, `C:\<PATH_TO_PYTHON>\Lib\site-packages\logtime-cli`), you'll find a file `config/config-default.ini`.

Copy that file to `config/config-user.ini`, and change that file as needed.

## Bash autocomplete
`click` builds an autocomplete script for us. To make use it, put the following in your .bashrc:

```
eval "$(_LT_COMPLETE=source lt)"
eval "$(_LOGTIME_COMPLETE=source logtime)"
```
