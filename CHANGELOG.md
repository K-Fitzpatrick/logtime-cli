# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased
## Added
- CLI option `--pie` that displays a pie chart of today's time log

## 1.2.0 - 2017-06-25
## Added
- Add CLI option to begin an entry by setting the start and end times to the current time. Intended to be continued later using the `-c` command.

## 1.1.0 - 2017-06-25
## Added
- Add CLI option to continue your last entry by updating its time

## 1.0.0 - 2017-06-10
## Added
- Option to leave out colon for `--start/--end` options: `01:15p` and `0115p` are the same
- Option to use military time for `--start/--end` options: `0115p` and `1315` are the same

### Changed
- CLI argument `--end` allows selecting an end-time for an entry, and replaces previous behavior of `lt 12:15 entry`
- CLI argument `--start` allows selecting a start-time for an entry, and replaces previous behavior of first argument in `lt 12:00p 12:15p entry`
- CLI argument `--previous` no longer creates a logfile that doesn't exist; instead, it displays a message to the user

## 0.6.0 - 2017-06-10
## Added
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
