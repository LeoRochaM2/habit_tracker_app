import pytest
from database import Database
from habits import DBHabit
from analytics import Analytics
from population import Population
import os



class TestHabitEdgeCases:
    """
    Tests edge cases for habit creation and related operations.

    Methods:
        setup_method: Initializes the test environment with a fresh database.
        test_create_habit_with_empty_name: Ensures a habit with an empty name cannot be created.
        test_duplicate_habit: Ensures duplicate habits are not allowed.
        test_boundary_dates: Validates adding events at date boundaries (end/start of the year).
        teardown_method: Cleans up resources after each test.
    """

    def setup_method(self):
        """Initializes a fresh test database."""
        self.db = Database("test.db")

    def test_create_habit_with_empty_name(self):
        """
        Ensures a habit with an empty name cannot be created.
        
        Expected:
            Returns a failure message indicating the name is invalid.
        """
        habit = DBHabit("", "test_description", "daily")
        result = habit.store(self.db)
        assert result == "Habit name cannot be blank or just whitespace. It was not added."

    def test_duplicate_habit(self):
        """
        Ensures duplicate habits are not allowed.
        
        Expected:
            Returns a failure message when attempting to create a habit with an existing name.
        """
        habit = DBHabit("test_habit", "test_description", "daily")
        habit.store(self.db)
        result = habit.store(self.db)
        assert result == "Habit 'test_habit' already exists. It was not added."

    def test_boundary_dates(self):
        """
        Validates adding events at date boundaries (end/start of the year).
        
        Expected:
            Events added on 2024-12-31 and 2025-01-01 are successfully recorded.
        """
        habit = DBHabit("test_habit_boundary", "test_description", "weekly")
        habit.store(self.db)

        result = habit.add_event(self.db, "2024-12-31")  # Last day of the year.
        assert "added" in result

        result = habit.add_event(self.db, "2025-01-01")  # First day of the new year.
        assert "added" in result

    def teardown_method(self):
        """Cleans up the database after each test."""
        self.db.connection.close()
        os.remove("test.db")

class TestAnalyticsEdgeCases:
    """
    Tests edge cases for analytics functionality.

    Methods:
        setup_method: Sets up an in-memory database and Analytics instance.
        test_empty_database: Ensures correct behavior with an empty database.
        test_partial_data: Tests streak calculation for a habit with no check-offs.
        test_longest_streak_ties: Ensures streak ties are handled correctly.
        teardown_method: Cleans up resources after each test.
    """

    def setup_method(self):
        """Sets up an in-memory database and initializes the Analytics object."""
        self.db = Database(":memory:")
        self.analytics = Analytics(self.db)

    def test_empty_database(self):
        """
        Ensures correct behavior with an empty database.

        Expected:
            No habits or streaks should be found.
        """
        habit_names = self.analytics.get_current_habit_names()
        assert habit_names == [], "Expected no habits in an empty database."

        longest_streaks = self.analytics.longest_streak_across()
        assert longest_streaks == [], "Expected no longest streaks in an empty database."

    def test_partial_data(self):
        """
        Tests streak calculation for a habit with no check-offs.

        Expected:
            Streak should be 0 for a habit with no check-offs.
        """
        habit = DBHabit("test_habit_partial", "test_description", "daily")
        habit.store(self.db)
        streak = self.analytics.calculate_streak("test_habit_partial")
        assert streak == 0, "Expected streak to be 0 for habit with no check-offs."

    def test_longest_streak_ties(self):
        """
        Ensures streak ties are handled correctly.

        Expected:
            All habits with the same longest streak are included in the result.
        """
        habit1 = DBHabit("habit1", "description1", "daily")
        habit2 = DBHabit("habit2", "description2", "daily")
        habit1.store(self.db)
        habit2.store(self.db)

        for date in ["2024-12-01 00:00:00", "2024-12-02 00:00:00", "2024-12-03 00:00:00"]:
            self.db.increment_tracker("habit1", date)
            self.db.increment_tracker("habit2", date)

        longest_streaks = self.analytics.longest_streak_across()
        assert len(longest_streaks) == 2
        assert ("habit1", 3) in longest_streaks
        assert ("habit2", 3) in longest_streaks

    def teardown_method(self):
        """Cleans up resources after each test."""
        self.db.connection.close()

class TestPopulation:
    """
    Tests the Population class for populating dummy data.

    Methods:
        setup_method: Sets up an in-memory database and Population instance.
        test_population_data: Ensures dummy data is correctly populated.
        test_population_no_duplicates: Ensures duplicate data is not added during re-population.
        teardown_method: Cleans up resources after each test.
    """

    def setup_method(self):
        """Sets up an in-memory database and initializes the Population object."""
        self.db = Database(":memory:")
        self.population = Population(self.db)

    def test_population_data(self):
        """
        Ensures dummy data is correctly populated.

        Expected:
            Habits are successfully added to the database.
        """
        self.population.populate_dummy_data()
        habit_names = [habit[1] for habit in self.db.get_current_habits()]
        assert len(habit_names) > 0, "Expected dummy data to populate habits."

    def test_population_no_duplicates(self):
        """
        Ensures duplicate data is not added during re-population.

        Expected:
            The database should contain no duplicate habits.
        """
        self.population.populate_dummy_data()
        self.population.populate_dummy_data()  # Populate again.

        cur = self.db.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM habit")
        habit_count = cur.fetchone()[0]
        assert habit_count == 5, "Expected no duplicate habits after re-population."

    def teardown_method(self):
        """Cleans up resources after each test."""
        self.db.connection.close()

class TestResetAndDeleteAll:
    """
    Tests reset and delete functionalities for habits and data.

    Methods:
        setup_method: Sets up an in-memory database and populates dummy data.
        test_reset_tracker: Tests resetting tracker data for a specific habit.
        test_delete_everything: Tests deleting all data from the database.
        teardown_method: Cleans up resources after each test.
    """

    def setup_method(self):
        """Sets up an in-memory database and populates it with dummy data."""
        self.db = Database(":memory:")
        self.population = Population(self.db)
        self.population.populate_dummy_data()

    def test_reset_tracker(self):
        """
        Tests resetting tracker data for a specific habit.

        Expected:
            Tracker data for the habit is cleared.
        """
        habit = DBHabit("workout", "test_description", "daily")
        habit.store(self.db)
        self.db.increment_tracker("workout", "2024-12-10")

        result = habit.reset_in_db(self.db)
        assert result == "All progress for habit 'workout' has been reset."

        data = self.db.get_habit_data("workout")
        assert len(data) == 0, "Expected tracker data to be cleared after reset."

    def test_delete_everything(self):
        """
        Tests deleting all data from the database.

        Expected:
            Both habit and tracker tables should be empty.
        """
        self.db.delete_db()
        cur = self.db.connection.cursor()

        cur.execute("SELECT COUNT(*) FROM habit")
        habit_count = cur.fetchone()[0]
        assert habit_count == 0, "Expected no habits after deleting all data."

        cur.execute("SELECT COUNT(*) FROM tracker")
        tracker_count = cur.fetchone()[0]
        assert tracker_count == 0, "Expected no tracker data after deleting all data."

    def teardown_method(self):
        """Cleans up resources after each test."""
        self.db.connection.close()



