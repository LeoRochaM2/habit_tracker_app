## Habit tracker project

## Description

The Habit Tracker project is a command-line application designed to help users track 
their habits effectively. It allows users to create, update, check off, analyze, 
and delete habits with either daily or weekly periodicities. 
The application includes features such as streak calculation, habit analysis, and more, 
all powered by an SQLite3 database backend.

## What It Is

- A CLI-based habit tracking application.
- Supports creating and managing habits with detailed descriptions.
- Calculates streaks for daily and weekly habits.
- Provides analysis features such as longest streaks and habit summaries.
- Includes test coverage and automatic dummy data population for development and testing.
- Built with object-oriented design and modular programming for scalability.

## Installation

To set up the Habit Tracker project, follow these steps:

Prerequisites:

Python 3.8 or newer must be installed.

1. 1. Clone the repository:
    ```Shell
    git clone <https://github.com/LeoRochaM2/habit_tracker_app.git>
    ``` 
1. 2. Navigate into the project directory:  
    ```Shell
    cd habit_tracker_app
    ```

2. Install the dependencies:
    ```Shell
    pip install -r requirements.txt
    ```

## Usage
Start

```Shell
python main_cli.py
```
Automatic Population of the Database:

- The app includes automatic population of the database with dummy data for testing and demonstration purposes.
- When you start the app for the first time, it checks if the database is empty and populates it with:
    - Sample daily and weekly habits.
    - Check-off events for streak and analytics demonstration for a 4 week period.

Follow the on-screen instructions to:

Create a New Habit:

- Choose "Create a new habit" from the menu.
- Provide the habit name, description, and periodicity (daily or weekly).
- Confirm, and the habit is stored in the database.

Check Off a Habit

- Select "Check off a habit" from the menu.
- Enter the habit name and an optional date (defaults to today).
- The app logs the event in the tracker.

Analyze Habits

- Choose "Analyze your habits" and select one of the following:
- View all currently tracked habits.
- Display habits grouped by periodicity.
- See the longest run streak across all habits.
- Analyze the longest streak for a specific habit.
- Retrieve all details about a habit.

Update a Habit

- Select "Update an existing habit."
- Enter the habit name and provide updated details (name, description, and/or periodicity).

Delete a Habit

- Choose "Delete a habit."
- Enter the name of the habit to permanently delete it and its data.

Reset the Habit Tracker

- Select "Reset the habit tracker."
- Clear all check-off events for a specific habit while retaining the habit itself.

Delete All Data

- Choose "Delete everything in the app."
- Permanently removes all data, resetting the app to its initial state.


## Tests

The project includes comprehensive tests to ensure all functionalities work as expected.

To run the test suite, execute:
```Shell
pytest .
```
This will:
- Validate habit creation, deletion, and updates.
- Test streak calculations for daily and weekly habits.
- Ensure the analytics features work correctly.

## License
This project is open source and available under the MIT License.

## Author
Leandro Rocha
