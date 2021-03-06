# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

## 2.0.0 - 2019-09-05
### Removed
- Support for Python <2.6

### Fixed
- Support special characters by opening files in UTF-8 encoding

## 1.6.1 - 2019-09-05
### Removed
- Support special characters by opening files in UTF-8 encoding; this unintentionally dropped support for Python <2.6 in v1.6.0 and will be added back in a later version

### Fixed
- Support for Python 2

## 1.6.0 - 2019-09-04
### Added
- CLI command `logtime section_report`, for printing all sections of a given name throughout your whole log history. Useful for "Summary" sections, or "Weekly report" sections. Doesn't support sections that appear in multiples in the same logfile.

### Fixed
- Support special characters by opening files in UTF-8 encoding

## 1.5.2 - 2019-08-30
### Fixed
- Support for some early versions of Python 2.6/2.7 restored

### Changed
- Document `lt --config` in README

## 1.5.1 - 2019-08-29
### Fixed
- Properly restrict installation to Python 2 or 3

## 1.5.0 - 2019-08-29
### Added
- Support for Python 3 (tested only on 3.7)

## 1.4.3 - 2019-08-29
### Fixed
- Properly restrict installation to `Python==2.*`
- Commands that interact with the "Notes" section now work properly when there is no extra newline between the last line of text and the "Time log" section header

## 1.4.2 - 2019-08-21
### Fixed
- `logtime list` now works perfectly fine when there are other random files/folders in the logfile directory

## 1.4.1 - 2019-08-21
### Added
- CLI command group `logtime`
- CLI command `logtime calc`, for calculating and displaying your logged time for the day
- CLI command `logtime count_tasks`, for displaying how many tasks you went through in the day
- CLI command `logtime list`, for displaying your logfiles and a number indicating how many days back it is, for use with the `-p` option for other commands
- CLI command `logtime summarize_week`, for displaying all Summary sections for the week
- CLI option `lt --recalc`, for recalculating the lengths of each of the days time entries

## 1.3.1 - 2017-11-21
### Fixed
- Setup.py can now find the statistics package

## 1.3.0 - 2017-11-21
### Added
- CLI option `--pie` that displays a pie chart of today's time log
- Instructions for activating bash autocompletion

## 1.2.0 - 2017-06-25
### Added
- CLI option `--begin` to begin an entry by setting the start and end times to the current time. Intended to be continued later using the `-c` command.

## 1.1.0 - 2017-06-25
### Added
- CLI option `--continue` to continue your last entry by updating its time

## 1.0.0 - 2017-06-10
### Added
- Option to leave out colon for `--start/--end` options: `01:15p` and `0115p` are the same
- Option to use military time for `--start/--end` options: `0115p` and `1315` are the same

### Changed
- CLI argument `--end` allows selecting an end-time for an entry, and replaces previous behavior of `lt 12:15 entry`
- CLI argument `--start` allows selecting a start-time for an entry, and replaces previous behavior of first argument in `lt 12:00p 12:15p entry`
- CLI argument `--previous` no longer creates a logfile that doesn't exist; instead, it displays a message to the user

## 0.6.0 - 2017-06-10
### Added
- Some scripts to automate releases

## 0.5.0 - 2017-05-26
### Added
- CLI help: `--help` or `-h`
- CLI argument `-p` to open yesterday's log file
- CLI argument `-p X` to open a log file `X` days in the past
- CLI argument `--config` to open the user config file
- CLI argument `--dir` to open the logfile directory

## 0.4.1 - 2017-05-26
### Added
- A config file
- Configurable new_day_start_time
- Configurable logfile_directory

## 0.3.0 - 2017-05-24
### Added
- Initial release
