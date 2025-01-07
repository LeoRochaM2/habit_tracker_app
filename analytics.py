from datetime import datetime


class Analytics:
    
    """Class analytics perform different analysis to the database."""
    
    def __init__(self, db):
        
        """
        Initializes the Analytics instance.

        Args:
            db (Database): db connection sqlite3.
        """
        
        self.db = db

    def calculate_count(self, habit_name):
        """
        Calculate the count of check-offs for a habit.

        Args:
            habit_name: The name of the habit(str).
        
        Returns:
            int: The number of check-offs for the habit.
        """
        data = self.db.get_habit_data(habit_name)
        return len(data)

    def get_current_habit_names(self):
        """
        Retrieve the names of all currently tracked habits.

        Returns:
            list: Names of all habits in the database.
        """
        habits = self.db.get_current_habits()
        return [habit[1] for habit in habits]

    def get_info(self, habit_name):
        """
        Retrieve and return all information about a habit.
        
        habit_name: The name of the habit(str).
        
        Returns:
            list or str: All habit details or a message if not found.
        """
        if self.db.proof_habit(habit_name):
            cur = self.db.connection.cursor()
            cur.execute("SELECT * FROM habit WHERE name = ?", (habit_name,))
            return cur.fetchall()
        else:
            return f"Habit '{habit_name}' not found."

    def get_periodicity(self, periodicity):
        """
        Retrieve the names of habits with the same periodicity.

        Args:
            periodicity: The periodicity of the habits.
        
        Returns:
            list: Names of habits with the specified periodicity.
        """
        cur = self.db.connection.cursor()
        cur.execute("SELECT name FROM habit WHERE periodicity = ?", (periodicity,))
        result = cur.fetchall()
        return [row[0] for row in result]

    def calculate_streak(self, habit_name):
        """
        Calculate the longest streak for a given habit.
        
        Args:
            habit_name: The name of the habit(str). 

        Returns:
            int or str: The longest streak for the habit or an error message.
        """
        if self.db.proof_habit(habit_name):
            cur = self.db.connection.cursor()

            # Fetch all check-off dates for the given habit
            cur.execute(
                "SELECT check_of_date FROM tracker WHERE habit_name = ? ORDER BY check_of_date ASC",
                (habit_name,),
            )
            check_off_dates = [row[0] for row in cur.fetchall()]

            if not check_off_dates:
                return 0  # No streaks if there are no check-offs

            # Determine periodicity of the habit
            cur.execute("SELECT periodicity FROM habit WHERE name = ?", (habit_name,))
            periodicity = cur.fetchone()[0]

            # Initialize streak counters
            longest_streak = 0
            current_streak = 1  # Start with the first check-off

            # Validate based on periodicity
            for i in range(1, len(check_off_dates)):
                current_date = datetime.strptime(check_off_dates[i], "%Y-%m-%d %H:%M:%S")
                previous_date = datetime.strptime(check_off_dates[i - 1], "%Y-%m-%d %H:%M:%S")

                if periodicity == "daily":
                    # Check if the current check-off is the next calendar day
                    if (current_date - previous_date).days == 1:
                        current_streak += 1
                    else:
                        # Update longest streak and reset current streak
                        longest_streak = max(longest_streak, current_streak)
                        current_streak = 1
                elif periodicity == "weekly":
                    # Check if the current check-off is in the next consecutive ISO week
                    current_week = current_date.isocalendar()[:2]  # (ISO year, ISO week)
                    previous_week = previous_date.isocalendar()[:2]

                    # Calculate if the current week is exactly one week after the previous week
                    if (current_week[0] == previous_week[0] and current_week[1] == previous_week[1] + 1) or \
                            (current_week[0] == previous_week[0] + 1 and previous_week[1] == 52 and current_week[1] == 1):
                        current_streak += 1
                    else:
                        # Update longest streak and reset current streak
                        longest_streak = max(longest_streak, current_streak)
                        current_streak = 1

            # Final streak comparison after the loop
            longest_streak = max(longest_streak, current_streak)

            return longest_streak
        else:
            return f"Habit '{habit_name}' not found."

    def longest_streak_across(self):
        """
        Calculate the longest streak across all habits.

        Returns:
            list: Tuples containing habit names and their longest streak.
        """
        cur = self.db.connection.cursor()
        cur.execute("SELECT name FROM habit")
        all_habits = [row[0] for row in cur.fetchall()]

        longest_streak = 0
        habits_with_longest_streak = []

        for habit_name in all_habits:
            streak = self.calculate_streak(habit_name)  # Use the existing calculate_streak function
            if streak > longest_streak:
                longest_streak = streak
                habits_with_longest_streak = [(habit_name, streak)]
            elif streak == longest_streak:
                habits_with_longest_streak.append((habit_name, streak))

        return habits_with_longest_streak
