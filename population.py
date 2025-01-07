from database import Database
from habits import DBHabit


class Population:
    
    """
    Handles the population of dummy data into the Habit Tracker application.

    Attributes:
        db (Database): The database instance to interact with.
    """

    def __init__(self, db: Database):
        """
        Initializes the Population class.

        Args:
            db (Database): An instance of the Database class for interacting with the database.
        """
        self.db = db

    def populate_dummy_data(self):
        """
        Populates the database with dummy habits and associated check-off events.

        Functionality:
            Adds predefined dummy habits to the `habit` table.
            Adds associated check-off events for each habit to the `tracker` table.

        Dummy Data:
            Includes daily and weekly habits with descriptive names and periodicities.
            Check-offs are added with specific dates and times to simulate user activity.
        """
        # Define dummy habits with name, description, periodicity, and creation date.
        habits = [
            ("workout", "Exercise daily", "daily", "2024-12-01 09:00:00"),
            ("car wash", "Wash the car weekly", "weekly", "2024-12-01 09:00:00"),
            ("meditation", "Meditate every day", "daily", "2024-12-01 09:00:00"),
            ("grocery shop", "Shop weekly", "weekly", "2024-12-01 09:00:00"),
            ("studying", "Study 30 minutes daily", "daily", "2024-12-01 09:00:00"),
        ]
        # Store each habit in the database
        for name, description, periodicity, date in habits:
            habit = DBHabit(name, description, periodicity)
            habit.store(self.db)

        # Add check-offs for workout (daily habit)
        workout_checkoffs = [
            f"2024-12-{day:02d} 07:00:00" for day in range(1, 31) if day not in {16, 19}
        ]
        self._add_checkoffs("workout", workout_checkoffs)

        # Add check-offs for meditation (daily habit)
        meditation_checkoffs = [
            f"2024-12-{day:02d} 07:00:00" for day in range(1, 31) if day not in {6, 13, 19}
        ]
        self._add_checkoffs("meditation", meditation_checkoffs)

        # Add check-offs for studying (daily habit)
        studying_checkoffs = [
            f"2024-12-{day:02d} 08:00:00" for day in range(1, 31) if day not in {15, 17, 22}
        ]
        self._add_checkoffs("studying", studying_checkoffs)

        # Add check-offs for car wash (weekly habit)
        car_wash_checkoffs = ["2024-12-02 15:00:00", "2024-12-09 15:00:00", "2024-12-23 15:00:00"]
        self._add_checkoffs("car wash", car_wash_checkoffs)

        # Add check-offs for grocery shop (weekly habit)
        grocery_checkoffs = ["2024-12-02 10:00:00", "2024-12-09 10:00:00", "2024-12-16 10:00:00"]
        self._add_checkoffs("grocery shop", grocery_checkoffs)

    def check_and_populate_dummy_data(self):
        
        """
        Checks if the database is empty and populates it with dummy data if needed.

        Returns:
            str: A message indicating whether dummy data was added or skipped.

        Functionality:
            Checks if there are any existing habits in the database using `get_current_habits`.
            If no habits are found:
                Calls `populate_dummy_data` to add dummy data.
                Returns a message indicating the database was populated.
            If habits are already present:
                Returns a message indicating no action was taken.
        """
        if not self.db.get_current_habits():  # Check if there are any habits
            self.populate_dummy_data()
            return "No data found in the database. Dummy data populated successfully."
        else:
            return "Database already populated. Skipping dummy data population."



    def _add_checkoffs(self, habit_name: str, checkoffs: list):
       
        """
        A helper method to add check-off events for a specific habit.

        Args:
            habit_name (str): The name of the habit to add check-offs for.
            checkoffs (list): A list of check-off dates (formatted as strings).

        Functionality:
            Iterates over the provided list of check-off dates.
            Logs each date in the `tracker` table using `increment_tracker`.
        """
        for date in checkoffs:
            self.db.increment_tracker(habit_name, date)
