from database import Database
from habits import DBHabit
from analytics import Analytics
from tabulate import tabulate
from population import Population
import questionary


class HabitTrackerCLI:
    """
    A Command Line Interface (CLI) for managing habits in the Habit Tracker application.

    Attributes:
        db (Database): Manages interaction with the SQLite database.
        population (Population): Handles population of the database with dummy data.
        analytics (Analytics): Provides methods for analyzing habit data.
    """
    def __init__(self):
        """
        Initializes the CLI with database, population, and analytics modules.
        """
        self.db = Database("habits.db")  # Connect to the database.
        self.population = Population(self.db)  # Initialize the Population class for dummy data handling.
        self.analytics = Analytics(self.db)  # Initialize the Analytics class for habit data analysis.

    def run(self):
        """
        Starts the CLI application loop, providing options for users to interact with the Habit Tracker.
        """
        # Populate the database with dummy data if empty.
        population_message = self.population.check_and_populate_dummy_data()
        print(population_message)
        questionary.confirm("Are you ready to start?").ask()

        # main loop for the CLI
        stop = False
        while not stop:
            # present the user with a list of options
            choice = questionary.select(
                "What would you like to do?",
                choices=[
                    "Create a new habit",
                    "Check off a habit",
                    "Analyse your habits",
                    "Update an existing habit",
                    "Delete a habit",
                    "Reset the habit tracker",
                    "Delete everything in the app",
                    "Exit"
                ]
            ).ask()

            # handle the user's choice
            if choice == "Create a new habit":
                self.create_habit()
            elif choice == "Check off a habit":
                self.check_off_habit()
            elif choice == "Analyse your habits":
                self.analyse_habits()
            elif choice == "Update an existing habit":
                self.update_habit()
            elif choice == "Delete a habit":
                self.delete_habit()
            elif choice == "Reset the habit tracker":
                self.reset_habit_tracker()
            elif choice == "Delete everything in the app":
                self.delete_all_data()
            else:
                print("Ciao, C U around! ;)")
                stop = True # exit the loop

    def create_habit(self):
        """
        Prompts the user to create a new habit with name, description, and periodicity.
        """
        # Gather inputs from the user.
        name = questionary.text("What's the name of your habit?").ask().strip().lower()
        desc = questionary.text("Describe your habit").ask()
        periodicity = questionary.select(
            "Choose the periodicity:",
            choices=["daily", "weekly"]
        ).ask()
        # Create and store the habit.
        
        habit = DBHabit(name=name, description=desc, periodicity=periodicity)
        response = habit.store(self.db)
        print(response)

    def check_off_habit(self):
        """
        Prompts the user to mark a habit as completed for a specific date.
        """
        # Gather inputs from the user.
        name = questionary.text("What's the name of the habit to check off?").ask().strip().lower()
        date = questionary.text("Enter the date (YYYY-MM-DD) or leave blank for today:").ask()
        # log the event
        habit = DBHabit(name=name, description="No description")
        response = habit.add_event(self.db, date if date else None)
        print(response)

    def analyse_habits(self):
        """
        Provides various analytics options for the user to analyze habit data.
        """
        # Present analytics options.
        choice = questionary.select("What would you like to analyse?",
                                    choices=[
                                        "Return all currently tracked habits",
                                        "Return all habits with the same periodicity",
                                        "Return the longest run streak of all habits",
                                        "Return the longest run streak for a given habit",
                                        "Return all information about a habit"
                                    ]).ask()
        # Call the corresponding analytics method.
        if choice == "Return all currently tracked habits":
            self.display_tracked_habits()
        elif choice == "Return all habits with the same periodicity":
            self.display_habits_with_same_periodicity()
        elif choice == "Return the longest run streak of all habits":
            self.display_longest_run_streak()
        elif choice == "Return the longest run streak for a given habit":
            self.display_longest_run_streak_for_habit()
        elif choice == "Return all information about a habit":
            self.display_habit_info()

    def update_habit(self):
        """
        Allows the user to update a habit's name, description, or periodicity.
        """
        # Gather inputs for the habit to update.
        name = questionary.text("Enter the name of the habit to update:").ask().strip().lower()
        habit = DBHabit(name, "no description")
        
        # prompt the user for new habit details
        new_name = questionary.text("Enter the new name for the habit (leave blank to keep the same):").ask().strip().lower()
        new_description = questionary.text("Enter the new description (leave blank to keep the same):").ask()
        new_periodicity = questionary.select(
            "Select the new periodicity (leave blank to keep the same):",
            choices=["daily", "weekly", ""]
        ).ask()

        # Update the habit with the new details.
        response = habit.update(
            self.db,
            new_name=new_name if new_name else None,
            new_description=new_description if new_description else None,
            new_periodicity=new_periodicity if new_periodicity else None,
        )
        print(response)

    def delete_habit(self):
        """
        Prompts the user to delete a habit and its associated tracker data.
        """
        name = questionary.text("Enter the name of the habit to delete:").ask().strip().lower()
        habit = DBHabit(name, "no description")
        response = habit.delete(self.db)
        print(response)

    def reset_habit_tracker(self):
        """
        Prompts the user to reset the tracker data for a specific habit.
        """
        name = questionary.text("Enter the name of the habit to reset:").ask().strip().lower()
        habit = DBHabit(name, "no description")
        response = habit.reset_in_db(self.db)
        print(response)

    def delete_all_data(self):
        """
        Deletes all habits and tracker data after user confirmation.
        """
        confirm1 = questionary.confirm("Are you absolutely sure you want to delete all data?").ask()
        if confirm1:
            confirm2 = questionary.confirm("This action cannot be undone. Proceed?").ask()
            if confirm2:
                response = self.db.delete_db()
                print(response)
            else:
                print("Operation canceled.")
        else:
            print("Operation canceled.")

    def display_tracked_habits(self):
        """
        Displays habits with the same periodicity (daily or weekly).
        """
        habits = self.analytics.get_current_habit_names()
        if habits:
            print("\nCurrently tracked habits:")
            print(tabulate([[habit] for habit in habits], headers=["Habit Names"], tablefmt="grid"))
        else:
            print("\nNo habits currently being tracked.")

    def display_habits_with_same_periodicity(self):
        """
        Displays all currently tracked habits in a tabular format.
        """
        periodicity = questionary.select(
            "Choose the periodicity:",
            choices=["daily", "weekly"]
        ).ask()

        habits = self.analytics.get_periodicity(periodicity)
        if habits:
            print("\nHabits with periodicity:", periodicity)
            print(tabulate([[habit] for habit in habits], headers=["Habit Name"], tablefmt="grid"))
        else:
            print(f"\nNo habits found with periodicity '{periodicity}'.")

    def display_longest_run_streak(self):
        """
        Displays the longest streak across all habits.
        """
        streaks = self.analytics.longest_streak_across()
        if streaks:
            data = [[habit, streak] for habit, streak in streaks]
            print(tabulate(data, headers=["Habit Name", "Longest Streak"], tablefmt="grid"))
        else:
            print("No streak data available.")

    def display_longest_run_streak_for_habit(self):
        """
        Displays the longest streak of a specific habit.
        """
        name = questionary.text("Enter the name of the habit:").ask().strip().lower()
        response = self.analytics.calculate_streak(name)
        if isinstance(response, int):
            data = [[name.capitalize(), response]]
            print(tabulate(data, headers=["Habit Name", "Longest Streak"], tablefmt="grid"))
        else:
            print(response)

    def display_habit_info(self):
        """
        Displays all stored information about a specific habit.
        """
        name = questionary.text("Enter the name of the habit:").ask().strip().lower()
        response = self.analytics.get_info(name)
        if isinstance(response, str):
            print(response)
        else:
            print(tabulate(response, headers=["Id", "Name", "Description", "Periodicity", "Creation date"], tablefmt="grid"))


if __name__ == "__main__":
    cli = HabitTrackerCLI()
    cli.run()
