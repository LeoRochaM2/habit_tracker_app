from database import Database
from habits import DBHabit
from analytics import Analytics
from datetime import datetime
import os



class TestHabit:
    """
    A test suite for validating core functionalities of the Habit Tracker.

    Methods:
        setup_method: Sets up a test database and initializes test data.
        test_habit: Tests basic creation and initialization of a habit.
        test_store_habit: Ensures habits are stored correctly and duplicates are handled.
        test_add_event: Validates the addition of events to the tracker table.
        test_reset_tracker_data: Ensures tracker data can be reset for a specific habit.
        test_delete_habit: Ensures a habit and its related data can be deleted.
        test_update_habit: Tests the update functionality for habit details.
        teardown_method: Cleans up resources after each test.
    """

    def setup_method(self):
        """
        Initializes a test environment.

        Functionality:
            Creates a test database file.
            Stores a sample habit for testing.
            Adds dummy tracker data for the habit.
        """
        # Set up a test database.
        self.db = Database("test.db")

        # Define and store the habit.
        self.habit_name = "test_habit_1"
        self.habit = DBHabit(self.habit_name, "test_description_1", "daily")
        self.habit.store(self.db)

        # Add dummy tracker data for testing.
        self.db.increment_tracker(self.habit_name, "2024-12-15")
        self.db.increment_tracker(self.habit_name, "2024-12-16")
        self.db.increment_tracker(self.habit_name, "2024-12-17")
        self.db.increment_tracker(self.habit_name, "2024-12-19")
        self.db.increment_tracker(self.habit_name, "2024-12-20")
        self.db.increment_tracker(self.habit_name, "2024-12-21")

    def test_habit(self):
        """
        Tests basic creation and initialization of a habit.

        Functionality:
            Creates a new habit with a unique timestamp to ensure uniqueness.
            Stores the habit in the database.
        """
        habit_name = "test_habit_1_" + str(datetime.now().timestamp())
        habit = DBHabit(habit_name, "test_description_1", "weekly")
        habit.store(self.db)

    def test_store_habit(self):
        """
        Ensures habits are stored correctly and duplicates are handled.

        Expected:
            A habit with the same name cannot be stored twice.
        """
        result = self.habit.store(self.db)
        assert result == f"Habit '{self.habit_name}' already exists. It was not added."

    def test_add_event(self):
        """
        Validates the addition of events to the tracker table.

        Functionality:
            Adds an event for a habit on a specific date.
            Ensures duplicate events are not allowed.
        """
        date = "2024-12-10"

        # First attempt to add an event (should succeed).
        expected_date = f"{date} 00:00:00"  # Match the format returned by add_event.
        result = self.habit.add_event(self.db, date)
        assert result == f"Event for habit '{self.habit_name}' added on {expected_date}."

        # Verify the event is in the tracker.
        data = self.db.get_habit_data(self.habit_name)
        assert len(data) == 7  # 6 pre-added events + 1 new event.
        assert data[-1][1] == expected_date  # Check the date of the event.

        # Second attempt to add the same event (should fail).
        result = self.habit.add_event(self.db, date)
        assert result == f"Habit '{self.habit_name}' was already checked-off on {date}."

        # Verify the tracker data hasn't changed.
        updated_data = self.db.get_habit_data(self.habit_name)
        assert len(updated_data) == len(data)

    def test_reset_tracker_data(self):
        """
        Ensures tracker data can be reset for a specific habit.

        Functionality:
            Resets all tracker data for the habit.
            Verifies the tracker data is cleared.
        """
        self.habit.add_event(self.db, "2024-12-15")
        self.habit.add_event(self.db, "2024-12-16")
        result = self.habit.reset_in_db(self.db)
        assert result == f"All progress for habit '{self.habit_name}' has been reset."

        # Verify tracker data is cleared.
        data = self.db.get_habit_data(self.habit_name)
        assert len(data) == 0

    def test_delete_habit(self):
        """
        Ensures a habit and its related data can be deleted.

        Functionality:
            Deletes the habit and its tracker data.
            Verifies the habit and tracker data are removed from the database.
        """
        result = self.habit.delete(self.db)
        assert result == f"The habit '{self.habit_name}' has been deleted."

        # Verify habit and tracker data are removed.
        cur = self.db.connection.cursor()
        cur.execute("SELECT * FROM habit WHERE name = ?", (self.habit_name,))
        habit_data = cur.fetchall()
        assert len(habit_data) == 0

        cur.execute("SELECT * FROM tracker WHERE habit_name = ?", (self.habit_name,))
        tracker_data = cur.fetchall()
        assert len(tracker_data) == 0

    def test_update_habit(self):
        """
        Tests the update functionality for habit details.

        Functionality:
            Updates the habit name, description, and periodicity.
            Verifies the updated details in the database.
        """
        new_name = "updated_habit"
        new_description = "updated_description"
        new_periodicity = "weekly"
        result = self.habit.update(self.db, new_name, new_description, new_periodicity)
        assert result == f"Habit '{new_name}' has been updated successfully."

        # Verify the habit is updated.
        cur = self.db.connection.cursor()
        cur.execute("SELECT * FROM habit WHERE name = ?", (new_name,))
        updated_habit = cur.fetchone()
        assert updated_habit is not None
        assert updated_habit[1] == new_name
        assert updated_habit[2] == new_description
        assert updated_habit[3] == new_periodicity

    def teardown_method(self):
        """
        Cleans up resources after each test.

        Functionality:
            Closes the database connection.
            Deletes the test database file.
        """
        self.db.connection.close()
        os.remove("test.db")





