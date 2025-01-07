import sqlite3
from datetime import datetime

class Database:
    def __init__(self, name="main.db"):
       
        """Initialize the database connection and create tables if they don't exist."""
        
        self.connection = sqlite3.connect(name)
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()

    def create_tables(self):
        
        """Create the necessary tables in the database."""
        
        cur = self.connection.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS habit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL, 
                description TEXT, 
                periodicity TEXT NOT NULL,
                date TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS tracker (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_of_date TEXT,
                habit_name TEXT NOT NULL,
                FOREIGN KEY (habit_name) REFERENCES habit (name) ON UPDATE CASCADE ON DELETE CASCADE
            )
        ''')
        self.connection.commit()

    def add_habit(self, name, description, periodicity, date):
        """
        Add a new habit to the habit table.
        
        Args:
            name (str): The name of the habit.
            description (str): A description of the habit.
            periodicity (str): The periodicity of the habit (daily or weekly).
            date (str): The date the habit was added.(if no values are provided, the current date is used)
        
        Returns  str: A message indicating the success or failure of the operation.
        """
        cur = self.connection.cursor()
        name = name.strip().lower()
        
        if not name:
            return "Error: Habit name cannot be empty or just whitespace."
        if not description.strip():
            description = "No description"  # Default description if not provided
        
        # Check for duplicate habit (case-insensitive)
        cur.execute("SELECT COUNT(*) FROM habit WHERE LOWER(name) = LOWER(?)", (name,))
        if cur.fetchone()[0] > 0:
            return f"Error: A habit with the name '{name}' already exists."
        
        try:
            cur.execute(
                "INSERT INTO habit (name, description, periodicity, date) VALUES (?, ?, ?, ?)",
                (name, description, periodicity, date)
            )
            self.connection.commit()
            return f"Habit '{name}' added successfully."
        except Exception as e:
            return f"Error adding habit: {e}"

    def increment_tracker(self, habit_name, event_date=None):
        """
        Add an event to the tracker table.
        Args:
            habit_name (str): The name of the habit.
            event_date (str): The date of the event. Defaults to the current date and time.
            
        Returns:
            str: A message indicating the success or failure of the operation.    
        """
        
        cur = self.connection.cursor()
        if not event_date:
            event_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Validate that the habit exists in a case-insensitive manner
        cur.execute("SELECT name FROM habit WHERE LOWER(name) = LOWER(?)", (habit_name,))
        matched_habit = cur.fetchone()

        if not matched_habit:
            return f"Habit '{habit_name}' not found. Cannot add event."

        habit_name = matched_habit[0]

        try:
            cur.execute(
                "INSERT INTO tracker (habit_name, check_of_date) VALUES (?, ?)",
                (habit_name, event_date)
            )
            self.connection.commit()
            return f"Event for habit '{habit_name}' added on {event_date}."
        except sqlite3.IntegrityError as e:
            return f"Error adding event: {e}"

    def get_habit_data(self, habit_name):
        
        """Retrieve all tracker data for a specific habit."""
        
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM tracker WHERE habit_name=?", (habit_name,))
        return cur.fetchall()

    def delete_habit_data(self, habit_name):
        """
        Delete all data related to a specific habit in both DBs.
        
        Args:
            habit_name (str): The name of the habit.
        
        Returns:
            str: A message indicating the success or failure of the operation.
        """
        
        cur = self.connection.cursor()
        cur.execute("DELETE FROM tracker WHERE habit_name = ?", (habit_name,))
        cur.execute("DELETE FROM habit WHERE name = ?", (habit_name,))
        self.connection.commit()

    def proof_habit(self, habit_name):
        """
        Check if a habit exists for operations where a specific habit is needed.
        
        Args:
            habit_name (str): The name of the habit.
        
        Returns:
            bool: True if the habit exists, False otherwise.
        """
        
        cur = self.connection.cursor()
        cur.execute("SELECT COUNT(*) FROM habit WHERE LOWER(name) = LOWER(?)", (habit_name,))
        return cur.fetchone()[0] > 0

    def update_habit(self, old_name, new_name=None, new_description=None, new_periodicity=None):
        """
        Update habit details in the database: name and/or desc. and/or periodicity.
        
        Args:
            old_name (str): The current name of the habit.
            new_name (str): The new name of the habit.
            new_description (str): The new description of the habit.
            new_periodicity (str): The new periodicity of the habit.
        Returns:
            str: A message indicating the success or failure of the operation.
        """
        
        cur = self.connection.cursor()
        cur.execute("SELECT name FROM habit WHERE LOWER(name) = LOWER(?)", (old_name,))
        existing_name = cur.fetchone()

        if not existing_name:
            return f"Habit '{old_name}' not found. Cannot update."

        exact_name = existing_name[0]

        if new_name:
            cur.execute("UPDATE habit SET name = ? WHERE name = ?", (new_name, exact_name))
            exact_name = new_name
        if new_description:
            cur.execute("UPDATE habit SET description = ? WHERE name = ?", (new_description, exact_name))
        if new_periodicity:
            cur.execute("UPDATE habit SET periodicity = ? WHERE name = ?", (new_periodicity, exact_name))

        self.connection.commit()
        return f"Habit '{exact_name}' has been updated successfully."

    def delete_tracker_data(self, habit_name):
        """
        Delete tracker data for a specific habit.
        
        Args:
            habit_name (str): The name of the habit.
        
        Returns:
            str: A message indicating the success or failure of the operation.    
        """
        
        cur = self.connection.cursor()
        cur.execute("DELETE FROM tracker WHERE habit_name = ?", (habit_name,))
        self.connection.commit()

    def get_current_habits(self):
        """
        Retrieve all habits from the database.
        
        Returns:
            list: A list of all habits in the database.
        """
        
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM habit")
        return cur.fetchall()

    def delete_db(self):
        """
        Delete all data from the database.
        
        Returns:
            str: A message indicating the success or failure of the operation.
        """
        try:
            cur = self.connection.cursor()
            cur.execute("DELETE FROM tracker")
            cur.execute("DELETE FROM habit")
            self.connection.commit()
            return "All data has been successfully deleted."
        except Exception as e:
            return f"An error occurred while deleting data: {e}"

    def get_habit_periodicity(self, habit_name):
        """
        Retrieve the periodicity of a habit.
        
        Args:
            habit_name (str): The name of the habit.
        
        Returns:
            str: The periodicity of the habit.
        """
        cur = self.connection.cursor()
        cur.execute("SELECT periodicity FROM habit WHERE LOWER(name) = LOWER(?)", (habit_name,))
        result = cur.fetchone()
        return result[0] if result else None

    def check_event_exists(self, habit_name, event_date, periodicity):
        """
        Check if an event already exists for the given habit and date.
        
        Args:
            habit_name (str): The name of the habit.
            event_date (str): The date of the event.
            periodicity (str): The periodicity of the habit.
        
        Returns:
            bool: True if the event exists, False otherwise.
        """
        cur = self.connection.cursor()
        if periodicity == "daily":
            cur.execute(
                '''
                SELECT COUNT(*) FROM tracker
                WHERE habit_name = ? AND DATE(check_of_date) = DATE(?)
                ''',
                (habit_name, event_date)
            )
        elif periodicity == "weekly":
            cur.execute(
                '''
                SELECT COUNT(*) FROM tracker
                WHERE habit_name = ? AND strftime('%Y-%W', check_of_date) = strftime('%Y-%W', ?)
                ''',
                (habit_name, event_date)
            )
        return cur.fetchone()[0] > 0

    """def get_all_habits(self):
        
        ""Retrieve all habits.""
        
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM habit")
        return cur.fetchall()"""

    def close(self):
        
        """Close the database connection."""
        
        self.connection.close()
