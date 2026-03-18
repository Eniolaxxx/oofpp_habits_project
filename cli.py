# cli.py
# main file - run this to start the habit tracker
# shows a simple menu for the user to interact with

from datetime import datetime
from database import setup, add_habit, remove_habit, add_completion, get_all_habits, name_exists
from habit import Habit
from analytics import all_habits, habits_by_period, best_streak_overall, best_streak_for, get_streak, struggled_habits

def show_habits(habits):
    if not habits:
        print("  No habits found.")
        return
    print(f"  {'ID':<5} {'Name':<25} {'Period':<10} {'Streak'}")
    print("  " + "-" * 50)
    for h in habits:
        print(f"  {h.habit_id:<5} {h.name:<25} {h.periodicity:<10} {get_streak(h)} days/weeks")

def create_habit():
    print("\n-- Create Habit --")
    name = input("  Name: ").strip()
    if not name:
        print("  Name cant be empty!")
        return
    if name_exists(name):
        print("  That habit already exists.")
        return
    desc = input("  Description: ").strip()
    while True:
        period = input("  Daily or weekly? ").strip().lower()
        if period in ["daily", "weekly"]:
            break
        print("  Please type daily or weekly")
    
    h = Habit(name, desc, period)
    new_id = add_habit(h)
    print(f"  Habit created! ID = {new_id}")

def checkoff():
    print("\n-- Check Off Habit --")
    habits = get_all_habits()
    if not habits:
        print("  No habits yet.")
        return
    show_habits(habits)
    try:
        hid = int(input("\n  Enter habit ID: "))
    except:
        print("  Invalid input.")
        return
    
    match = [h for h in habits if h.habit_id == hid]
    if not match:
        print("  Habit not found.")
        return
    
    ts = datetime.now().isoformat()
    add_completion(hid, ts)
    print(f"  Done! {match[0].name} checked off.")

def delete_habit():
    print("\n-- Delete Habit --")
    habits = get_all_habits()
    if not habits:
        print("  No habits to delete.")
        return
    show_habits(habits)
    try:
        hid = int(input("\n  Enter habit ID to delete: "))
    except:
        print("  Invalid input.")
        return
    
    match = [h for h in habits if h.habit_id == hid]
    if not match:
        print("  Habit not found.")
        return
    
    confirm = input(f"  Delete '{match[0].name}'? yes/no: ").strip().lower()
    if confirm == "yes":
        remove_habit(hid)
        print("  Deleted.")
    else:
        print("  Cancelled.")

def analytics():
    while True:
        print("\n-- Analytics --")
        print("  1. All habits summary")
        print("  2. Daily habits only")
        print("  3. Weekly habits only")
        print("  4. Best streak overall")
        print("  5. Best streak for one habit")
        print("  6. Habits I struggle with")
        print("  0. Back")
        
        choice = input("\n  Choose: ").strip()
        habits = get_all_habits()
        
        if choice == "0":
            break
        elif choice == "1":
            show_habits(habits)
        elif choice == "2":
            show_habits(habits_by_period(habits, "daily"))
        elif choice == "3":
            show_habits(habits_by_period(habits, "weekly"))
        elif choice == "4":
            h, s = best_streak_overall(habits)
            if h:
                print(f"  Best: {h.name} with streak of {s}")
            else:
                print("  No habits found.")
        elif choice == "5":
            show_habits(habits)
            try:
                hid = int(input("  Enter ID: "))
            except:
                print("  Invalid.")
                continue
            match = [h for h in habits if h.habit_id == hid]
            if match:
                print(f"  Longest streak for {match[0].name}: {best_streak_for(match[0])}")
        elif choice == "6":
            result = struggled_habits(habits)
            for h in result:
                print(f"  - {h.name} ({h.periodicity})")
        else:
            print("  Invalid option.")

def main():
    setup()
    print("\n=== HABIT TRACKER ===")
    print("Track your daily and weekly habits\n")
    
    while True:
        print("\nMAIN MENU")
        print("1. Create habit")
        print("2. List habits")
        print("3. Check off habit")
        print("4. Delete habit")
        print("5. Analytics")
        print("0. Exit")
        
        choice = input("\nSelect: ").strip()
        
        if choice == "1":
            create_habit()
        elif choice == "2":
            habits = get_all_habits()
            show_habits(habits)
        elif choice == "3":
            checkoff()
        elif choice == "4":
            delete_habit()
        elif choice == "5":
            analytics()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
