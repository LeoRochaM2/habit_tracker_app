from database import Database
from analytics import Analytics
from population import Population  
from tabulate import tabulate
import sqlite3



class TestAnalytics:
    """
    A test suite for the Analytics class to validate its methods and functionalities.

    Methods:
        setup_method: Sets up an in-memory SQLite database with dummy data for testing.
        test_get_current_habit_names: Tests retrieval of all current habit names.
        test_get_info: Tests retrieval of detailed information for a specific habit.
        test_get_periodicity: Tests retrieval of habits based on their periodicity (daily/weekly).
        test_calculate_streak: Tests calculation of the longest streak for individual habits.
        test_longest_streak_across: Tests calculation of the longest streak across all habits.
        teardown_method: Cleans up resources after each test.
    """

    def setup_method(self):
        """
        Initializes the test environment.

        Functionality:
            Creates an in-memory SQLite database.
            Populates the database with dummy data using the Population class.
            Initializes an Analytics instance for testing.
        """
        # Use an in-memory SQLite database for testing.
        self.db = Database(":memory:")

        # Populate the database with dummy data.
        population = Population(self.db)
        population.populate_dummy_data()

        # Initialize the Analytics object for testing.
        self.analytics = Analytics(self.db)

    def test_get_current_habit_names(self):
        """
        Tests retrieval of all current habit names.

        Functionality:
            Calls `get_current_habit_names` to retrieve all habit names.
            Ensures the expected number of habits is retrieved.
        """
        habit_names = self.analytics.get_current_habit_names()
        print("\nCurrent Habit Names:")
        print(tabulate([[name] for name in habit_names], headers=["Habit Names"], tablefmt="grid"))
        assert len(habit_names) == 5  # Ensure 5 habits are loaded.

    def test_get_info(self):
        """
        Tests retrieval of detailed information for a specific habit.

        Functionality:
            Calls `get_info` for a habit name.
            Ensures the returned data matches the expected habit details.
        """
        habit_info = self.analytics.get_info("workout")
        print("\nInformation for 'workout':")
        print(tabulate(habit_info, headers=["ID", "Name", "Description", "Periodicity", "Date"]))
        assert len(habit_info) > 0
        assert habit_info[0][1] == "workout"

    def test_get_periodicity(self):
        """
        Tests retrieval of habits based on their periodicity.

        Functionality:
            Calls `get_periodicity` with "daily" and "weekly".
            Validates the returned habits for each periodicity.
        """
        daily_habits = self.analytics.get_periodicity("daily")
        print("\nDaily Habits:")
        print(tabulate([[habit] for habit in daily_habits], headers=["Habit Names"], tablefmt="grid"))
        assert len(daily_habits) == 3

        weekly_habits = self.analytics.get_periodicity("weekly")
        print("\nWeekly Habits:")
        print(tabulate([[habit] for habit in weekly_habits], headers=["Habit Names"], tablefmt="grid"))
        assert len(weekly_habits) == 2

    def test_calculate_streak(self):
        """
        Tests calculation of the longest streak for individual habits.

        Functionality:
            Calls `calculate_streak` for specific habits.
            Validates the returned streaks match expected values.
        """
        # Test streak for daily habits.
        longest_daily_streak = self.analytics.calculate_streak("meditation")
        print(f"\nLongest streak for 'meditation': {longest_daily_streak}")
        assert longest_daily_streak == 11  # Replace with actual dummy data assumption.

        longest_daily_streak = self.analytics.calculate_streak("studying")
        print(f"\nLongest streak for 'studying': {longest_daily_streak}")
        assert longest_daily_streak == 14  # Replace with actual dummy data assumption.

        longest_daily_streak = self.analytics.calculate_streak("workout")
        print(f"\nLongest streak for 'workout': {longest_daily_streak}")
        assert longest_daily_streak == 15  # Replace with actual dummy data assumption.

        # Test streak for weekly habits.
        weekly_streak = self.analytics.calculate_streak("car wash")
        print(f"\nLongest streak for 'car wash': {weekly_streak}")
        assert weekly_streak == 2  # Replace with actual dummy data assumption.

        weekly_streak = self.analytics.calculate_streak("grocery shop")
        print(f"\nLongest streak for 'grocery shop': {weekly_streak}")
        assert weekly_streak == 3  # Replace with actual dummy data assumption.

    def test_longest_streak_across(self):
        """
        Tests calculation of the longest streak across all habits.

        Functionality:
            Calls `longest_streak_across`.
            Ensures the returned list contains the correct streak values.
        """
        longest_streaks = self.analytics.longest_streak_across()  # Returns a list of (habit_name, streak) tuples.

        # Ensure the return type is correct.
        assert isinstance(longest_streaks, list), "The function should return a list of tuples."
        assert len(longest_streaks) > 0, "The function should return at least one habit with a streak."

        # Extract the streak value for validation.
        streak = longest_streaks[0][1]  # All streaks should match the longest one.

        # Print and validate the results.
        print("\nHabits with the longest streak:")
        for habit, habit_streak in longest_streaks:
            print(f"Habit: {habit}, Streak: {habit_streak}")
            assert self.analytics.calculate_streak(habit) == streak, (
                f"The streak for habit '{habit}' should match the reported longest streak."
            )

        # Validate that all streaks match the longest streak.
        for _, habit_streak in longest_streaks:
            assert habit_streak == streak, "All streaks should be equal to the longest streak."

    def teardown_method(self):
        """
        Cleans up resources after each test by closing the database connection.
        """
        if self.db.connection:
            self.db.close()

