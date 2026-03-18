# seed_data.py
# loads 5 example habits into the database for testing

from datetime import datetime, timedelta
from database import setup, add_habit, add_completion, name_exists
from habit import Habit
import random

def run():
    setup()
    
    start = datetime.now() - timedelta(weeks=4)
    
    habits = [
        {"name": "Drink 2L of Water", "desc": "Stay hydrated every day", "period": "daily"},
        {"name": "Morning Exercise", "desc": "At least 20 mins of exercise", "period": "daily"},
        {"name": "Read a Book", "desc": "Read at least 10 pages", "period": "daily"},
        {"name": "Weekly Meal Prep", "desc": "Prepare meals for the week", "period": "weekly"},
        {"name": "Review Weekly Goals", "desc": "Check progress on goals", "period": "weekly"},
    ]
    
    for data in habits:
        if name_exists(data["name"]):
            print(f"  [SKIP] {data['name']} already exists")
            continue
        
        h = Habit(data["name"], data["desc"], data["period"], created_at=start.isoformat())
        hid = add_habit(h)
        
        # add some completions over 4 weeks
        count = 0
        if data["period"] == "daily":
            for i in range(28):
                # sometimes miss a day
                if random.random() > 0.15:
                    ts = start + timedelta(days=i, hours=random.randint(7, 21))
                    add_completion(hid, ts.isoformat())
                    count += 1
        else:
            for i in range(4):
                if random.random() > 0.2:
                    ts = start + timedelta(weeks=i, days=random.randint(0, 6))
                    add_completion(hid, ts.isoformat())
                    count += 1
        
        print(f"  [OK] {data['name']} - {count} completions")
    
    print("\nDone!")

if __name__ == "__main__":
    run()
