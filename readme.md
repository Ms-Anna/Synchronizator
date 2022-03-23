# **_One-way folder synchronizator_**

## What the project does
Synchronizes two folders: source and replica, specifically:
* Synchronization is one-way: after the synchronization content of the replica folder
is modified to exactly match content of the source folder;
* Synchronization performs periodically;
* File creation/copying/removal operations is logged to a file and to the console
output;

Folder paths, synchronization interval and log file path should be provided by user.

## How users can get started with the project
### Call example (for Windows):
```kotlin
python synchronizator.py [--sf <path_to_source_folder>] [--rf <path_to_replica_folder>] [--i <sync_interval>] [--lf <path_to_log_file>]
```

\* for Linux use "python3" instead of "python"

If no arguments are provided, they will be requested.

Required arguments:
* [--sf <path_to_source_folder>] - path to the source folder that will be replicated;
* [--rf <path_to_replica_folder>] - path to the replica folder where the source folder will be replicated;
* [--i <sync_interval>] - synchronization interval, should be positive whole-number (minutes by default);
* [--lf <path_to_log_file>] - path and name to the file to log creation/copying/removal operations.

Optional arguments:
* [--tm <h || m || d>] - choices for time-measuring (h - hour; m - minute; d - day), default='m'.

The project was implemented and may be run with Python 3.9.0. Compatibility with previous Python versions has not been verified.
