# Habit Tracker

A simple habit tracking app built with Python for the IU portfolio assignment (DLBDSOOFPP01).

## What it does
- Create daily and weekly habits
- Check off habits when you complete them
- Delete habits you no longer need
- Analyse your habit streaks and progress

## Requirements
- Python 3.7 or higher
- No extra libraries needed (uses built-in sqlite3)

## How to install
1. Download and extract the project folder
2. Open a terminal and go to the folder:
```
cd habit_tracker
```

## How to run

First load the example habits:
```
py seed_data.py
```

Then start the app:
```
py cli.py
```

## How to run tests
```
py -m pytest test_habits.py -v
```

## Files
- habit.py - the Habit class
- database.py - saves/loads data using sqlite3
- analytics.py - functions to analyse habits
- cli.py - the main menu
- seed_data.py - loads 5 example habits
- test_habits.py - unit tests

## Predefined habits
| Name | Type |
|------|------|
| Drink 2L of Water | Daily |
| Morning Exercise | Daily |
| Read a Book | Daily |
| Weekly Meal Prep | Weekly |
| Review Weekly Goals | Weekly |
