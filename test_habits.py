# test_habits.py
# basic tests to check the habit tracker works correctly
# run with: python -m pytest test_habits.py -v

import unittest
import os
from datetime import datetime, timedelta
from habit import Habit
from database import setup, add_habit, remove_habit, add_completion, get_all_habits, name_exists
from analytics import all_habits, habits_by_period, best_streak_overall, best_streak_for, get_streak, get_longest

TEST_DB = "test.db"

class TestHabit(unittest.TestCase):

    def test_make_daily_habit(self):
        h = Habit("Test", "testing", "daily")
        self.assertEqual(h.name, "Test")
        self.assertEqual(h.periodicity, "daily")

    def test_make_weekly_habit(self):
        h = Habit("Weekly", "test", "weekly")
        self.assertEqual(h.periodicity, "weekly")

    def test_bad_period_raises_error(self):
        with self.assertRaises(ValueError):
            Habit("Bad", "test", "monthly")

    def test_checkoff(self):
        h = Habit("Test", "test", "daily")
        h.check_off()
        self.assertEqual(len(h.completions), 1)

    def test_checkoff_with_time(self):
        h = Habit("Test", "test", "daily")
        h.check_off("2024-01-01T10:00:00")
        self.assertEqual(h.completions[0], "2024-01-01T10:00:00")


class TestDatabase(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        setup(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_habit(self):
        h = Habit("Water", "drink water", "daily")
        hid = add_habit(h, TEST_DB)
        self.assertIsNotNone(hid)

    def test_load_habits(self):
        add_habit(Habit("H1", "d", "daily"), TEST_DB)
        add_habit(Habit("H2", "d", "weekly"), TEST_DB)
        result = get_all_habits(TEST_DB)
        self.assertEqual(len(result), 2)

    def test_delete_habit(self):
        hid = add_habit(Habit("Delete", "d", "daily"), TEST_DB)
        remove_habit(hid, TEST_DB)
        result = get_all_habits(TEST_DB)
        self.assertEqual(len(result), 0)

    def test_name_check(self):
        add_habit(Habit("Unique", "d", "daily"), TEST_DB)
        self.assertTrue(name_exists("Unique", TEST_DB))
        self.assertFalse(name_exists("NotThere", TEST_DB))

    def test_completion_saved(self):
        hid = add_habit(Habit("Water", "d", "daily"), TEST_DB)
        add_completion(hid, "2024-03-01T09:00:00", TEST_DB)
        habits = get_all_habits(TEST_DB)
        self.assertEqual(len(habits[0].completions), 1)


class TestAnalytics(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        setup(TEST_DB)
        
        today = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        # daily habit with 7 day streak
        self.h1 = Habit("Water", "drink", "daily")
        hid = add_habit(self.h1, TEST_DB)
        self.h1.habit_id = hid
        for i in range(7):
            ts = (today - timedelta(days=6-i)).isoformat()
            add_completion(hid, ts, TEST_DB)
            self.h1.completions.append(ts)
        
        # weekly habit
        self.h2 = Habit("Meal Prep", "prep", "weekly")
        hid2 = add_habit(self.h2, TEST_DB)
        self.h2.habit_id = hid2
        for i in range(3):
            ts = (today - timedelta(weeks=2-i)).isoformat()
            add_completion(hid2, ts, TEST_DB)
            self.h2.completions.append(ts)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_all_habits(self):
        habits = get_all_habits(TEST_DB)
        self.assertEqual(len(all_habits(habits)), 2)

    def test_filter_daily(self):
        habits = get_all_habits(TEST_DB)
        daily = habits_by_period(habits, "daily")
        self.assertEqual(len(daily), 1)

    def test_filter_weekly(self):
        habits = get_all_habits(TEST_DB)
        weekly = habits_by_period(habits, "weekly")
        self.assertEqual(len(weekly), 1)

    def test_streak(self):
        self.assertEqual(get_streak(self.h1), 7)

    def test_longest(self):
        self.assertEqual(get_longest(self.h1), 7)

    def test_best_overall(self):
        habits = get_all_habits(TEST_DB)
        h, s = best_streak_overall(habits)
        self.assertIsNotNone(h)
        self.assertGreater(s, 0)

    def test_empty_list(self):
        self.assertEqual(all_habits([]), [])
        self.assertEqual(habits_by_period([], "daily"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
