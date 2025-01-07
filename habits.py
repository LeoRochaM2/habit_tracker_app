from datetime import datetime


class Habit:
    
    """
    Represents a habit that can be tracked for daily or weekly progress.

    Attributes:
        id (int): A unique identifier for the habit. Default is None.
        name (str): The name of the habit, stored in lowercase without leading or trailing whitespace.
        description (str): A short description of the habit, stripped of leading or trailing whitespace.
        periodicity (str): The frequency of the habit, either "daily" or "weekly". Defaults to "daily".
        date (str): The creation date and time of the habit, formatted as 'YYYY-MM-DD HH:MM:SS'.
        count (int): A counter for tracking progress related to the habit. Starts at 0.
    """
    
    def __init__(self, name: str, description: str, periodicity: str = "daily", id: int = None):
        
        """
        Initializes a new Habit instance.

        Args:
            name (str): The name of the habit.
            description (str): A brief description of the habit.
            periodicity (str, optional): The frequency of the habit, either "daily" or "weekly".
                                         Defaults to "daily".
            id (int, optional): A unique identifier for the habit. Defaults to None.
        """
        self.id = id
        self.name = name.strip().lower()
        self.description = description.strip()
        self.periodicity = periodicity
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.count = 0

    def increment(self):
        """
        Increments the habit's progress counter by 1.

        Example:
            If count is 0, calling increment() will set count to 1.
        """
        self.count += 1
        
    def reset(self):
        """
        Resets the habit's progress counter to 0.

        Example:
            If count is 5, calling reset() will set count to 0.
        """
        self.count = 0

    def __str__(self):
        """
        Returns a string representation of the habit, including its name and progress counter.

        Returns:
            str: A string in the format "{name}: {count}".
        """
        return f"{self.name}: {self.count}"


class DBHabit(Habit):
    """
    Represents a database-integrated habit by extending the base Habit class.

    Inherits all attributes and methods from the Habit class and adds functionality
    for interacting with a database.

    Attributes:
        Inherits all attributes from the Habit class:
            id (int): A unique identifier for the habit.
            name (str): The name of the habit, normalized to lowercase and stripped of extra spaces.
            description (str): A short description of the habit.
            periodicity (str): The frequency of the habit, either "daily" or "weekly".
            date (str): The creation date and time of the habit.
            count (int): A counter for tracking progress related to the habit.
    """
    def __init__(self, name: str, description: str, periodicity: str = "daily", id: int = None):
        """
        Initializes a new DBHabit instance by extending the base Habit class.

        Args:
            name (str): The name of the habit.
            description (str): A brief description of the habit.
            periodicity (str, optional): The frequency of the habit, either "daily" or "weekly".
                                         Defaults to "daily".
            id (int, optional): A unique identifier for the habit. Defaults to None.
        """
        super().__init__(name, description, periodicity, id) # Initialize attributes using the parent class.

    def store(self, db):
        """
        Store habit data in the database.

        Args:
            db (Database): An instance of the Database class for database operations.

        Returns:
            str: A message indicating whether the habit was stored successfully.

        Functionality:
            Validates that the habit name is not empty or just whitespace.
            Ensures the description is not empty, providing a default if it is.
            Checks if the habit already exists in the database using the `proof_habit` method.
            If the habit exists:
                Returns a message indicating it was not added.
            If the habit does not exist:
                Calls `db.add_habit` to store the habit's data in the database.
                Returns a success message.
        """
        if not self.name.strip():
            return "Habit name cannot be blank or just whitespace. It was not added."
        if not self.description.strip():
            self.description = "No description"

        if db.proof_habit(self.name):
            return f"Habit '{self.name}' already exists. It was not added."
        else:
            return db.add_habit(self.name, self.description, self.periodicity, self.date)

    def add_event(self, db, date: str = None):
        """
        Add an event to the tracker table.

        Args:
            db (Database): An instance of the Database class for database operations.
            date (str, optional): The date of the event. If None, the current date and time is used.

        Returns:
            str: A message indicating whether the event was added successfully.

        Functionality:
            Validates that the habit exists in the database using `proof_habit`.
            If the date is not provided, sets it to the current timestamp.
            Ensures the date format is valid (`YYYY-MM-DD`).
            Determines the habit's periodicity using `get_habit_periodicity`.
            Checks if the habit has already been checked off for the given date or week:
                For daily habits: Checks the specific date.
                For weekly habits: Checks the ISO week.
            If already checked-off:
                Returns an appropriate message.
            If not checked-off:
                Calls `increment_tracker` to log the event.
        """
        if db.proof_habit(self.name):
            if not date:
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    date = f"{date} 00:00:00"
                except ValueError:
                    return f"Invalid date format: '{date}'. Please use YYYY-MM-DD."

            periodicity = db.get_habit_periodicity(self.name)
            if not periodicity:
                return f"Could not determine periodicity for habit '{self.name}'."

            already_checked = db.check_event_exists(self.name, date, periodicity)

            if already_checked:
                if periodicity == "daily":
                    return f"Habit '{self.name}' was already checked-off on {date[:10]}."
                elif periodicity == "weekly":
                    return f"Habit '{self.name}' was already checked-off in this week."

            return db.increment_tracker(self.name, date)
        else:
            return f"Habit '{self.name}' not found. Cannot add event."

    def delete(self, db):
        """
        Delete a habit and all its associated tracker data from the database.

        Args:
            db (Database): An instance of the Database class, providing methods to interact with the database.

        Returns:
            str: A message indicating whether the habit was successfully deleted or not found.

        Functionality:
             Verifies if the habit exists in the database using the `proof_habit` method.
             If the habit exists:
                 Calls the `delete_habit_data` method from the `db` instance to delete the habit and its associated data.
                 Returns a success message.
             If the habit does not exist:
                 Returns a message indicating the habit was not found or a potential typo.
        """
        
        if db.proof_habit(self.name):
            db.delete_habit_data(self.name) 
            return f"The habit '{self.name}' has been deleted."
        else:
            return f"Habit '{self.name}' not found or there may be a typo."

    def update(self, db, new_name=None, new_description=None, new_periodicity=None):
        """
        Update habit details in the database.

        Args:
            db (Database): An instance of the Database class for database operations.
            new_name (str, optional): The new name for the habit. Defaults to None.
            new_description (str, optional): The new description for the habit. Defaults to None.
            new_periodicity (str, optional): The new periodicity for the habit ("daily" or "weekly"). Defaults to None.

        Returns:
            str: A message indicating whether the habit was updated successfully or not found.

        Functionality:
            Verifies if the habit exists in the database using `proof_habit`.
            If the habit exists:
                Calls `update_habit` with the new values to update the habit's details.
                Returns a success message.
            If the habit does not exist:
                Returns a message indicating the habit was not found.
        """
        if not db.proof_habit(self.name):
            return f"Habit '{self.name}' does not exist."

        return db.update_habit(self.name, new_name, new_description, new_periodicity)

    def reset_in_db(self, db):
        """
        Reset tracker data for the habit.

        Args:
            db (Database): An instance of the Database class for database operations.

        Returns:
            str: A message indicating whether the tracker data was reset successfully or if the habit was not found.

        Functionality:
            Verifies if the habit exists in the database using `proof_habit`.
            If the habit exists:
                Calls `delete_tracker_data` to remove all tracker data for the habit.
                Returns a success message.
            If the habit does not exist:
                Returns a message indicating the habit was not found.
        """
        if db.proof_habit(self.name):
            db.delete_tracker_data(self.name)
            return f"All progress for habit '{self.name}' has been reset."
        else:
            return f"Habit '{self.name}' not found."
