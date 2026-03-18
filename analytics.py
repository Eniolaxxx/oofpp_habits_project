# analytics.py
# functions to analyse habit data
# using functional programming (filter, map, sorted)

from datetime import datetime, timedelta

def get_period(timestamp, periodicity):
    # converts a timestamp into a period key (day or week)
    dt = datetime.fromisoformat(timestamp)
    if periodicity == "daily":
        return dt.strftime("%Y-%m-%d")
    else:
        y, w, _ = dt.isocalendar()
        return f"{y}-W{w:02d}"

def get_streak(habit):
    # calculates the current streak for a habit
    if not habit.completions:
        return 0
    
    done = set(get_period(t, habit.periodicity) for t in habit.completions)
    today = datetime.now()
    streak = 0
    
    if habit.periodicity == "daily":
        current = today
        while True:
            key = current.strftime("%Y-%m-%d")
            if key in done:
                streak += 1
                current -= timedelta(days=1)
            else:
                break
    else:
        current = today
        while True:
            y, w, _ = current.isocalendar()
            key = f"{y}-W{w:02d}"
            if key in done:
                streak += 1
                current -= timedelta(weeks=1)
            else:
                break
    
    return streak

def get_longest(habit):
    # finds the longest streak ever for a habit
    if not habit.completions:
        return 0
    
    periods = sorted(set(get_period(t, habit.periodicity) for t in habit.completions))
    
    def to_date(key):
        if habit.periodicity == "daily":
            return datetime.strptime(key, "%Y-%m-%d")
        else:
            y, w = key.split("-W")
            return datetime.strptime(f"{y}-W{w}-1", "%Y-W%W-%w")
    
    dates = list(map(to_date, periods))
    step = timedelta(days=1) if habit.periodicity == "daily" else timedelta(weeks=1)
    
    best = 1
    current = 1
    for i in range(1, len(dates)):
        if dates[i] - dates[i-1] == step:
            current += 1
            if current > best:
                best = current
        else:
            current = 1
    
    return best

# --- main analytics functions ---

def all_habits(habits):
    # returns all habits
    return list(habits)

def habits_by_period(habits, periodicity):
    # filter habits by daily or weekly
    return list(filter(lambda h: h.periodicity == periodicity, habits))

def best_streak_overall(habits):
    # finds which habit has the longest streak
    if not habits:
        return None, 0
    results = list(map(lambda h: (h, get_longest(h)), habits))
    return max(results, key=lambda x: x[1])

def best_streak_for(habit):
    # longest streak for one specific habit
    return get_longest(habit)

def struggled_habits(habits):
    # habits with most missed periods
    def miss_rate(h):
        created = datetime.fromisoformat(h.created_at)
        now = datetime.now()
        if h.periodicity == "daily":
            total = max((now - created).days, 1)
        else:
            total = max((now - created).days // 7, 1)
        done = len(set(get_period(t, h.periodicity) for t in h.completions))
        return (total - done) / total
    
    return sorted(habits, key=miss_rate, reverse=True)[:3]
