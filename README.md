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
- Includes test coverage and dummy data population for development and testing.

## Installation
To set up the Habit Tracker project, follow these steps:

1. Clone the repository:
   ```Shell
   git clone <repository-url>
   cd habit-tracker
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
Follow the on-screen instructions to:
- Create new habits.
- Check off habits for the current or a specific date.
- Analyze habits for streaks and periodicity.
- Update or delete existing habits.
- Reset the tracker or delete all data.

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
