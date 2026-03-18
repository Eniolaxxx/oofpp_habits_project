# habit.py
# This file contains the Habit class which stores all info about a habit

from datetime import datetime

class Habit:
    # a habit has a name, description, and a period (daily or weekly)
    def __init__(self, name, description, periodicity, created_at=None, habit_id=None):
        
        if periodicity not in ["daily", "weekly"]:
            raise ValueError("periodicity must be daily or weekly")
        
        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.completions = []  # list of times the habit was completed
        
        # if no date given, use today
        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now().isoformat()

    # this marks the habit as done
    def check_off(self, timestamp=None):
        if timestamp:
            self.completions.append(timestamp)
        else:
            self.completions.append(datetime.now().isoformat())

    def __repr__(self):
        return f"Habit({self.name}, {self.periodicity}, completions={len(self.completions)})"
