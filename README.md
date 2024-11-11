# LKIT

A local contact management system with conversation tracking.

## Features
- Store and manage contact information
- Track conversations with contacts
- Local storage using JSON files
- Simple and intuitive interface

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`


## Building an Executable
To create a standalone executable:

1. Ensure you're using Python 3.11 (PyInstaller currently has issues with Python 3.12)
2. Install PyInstaller: `pip install pyinstaller`
3. Create the executable: `pyinstaller --name LKIT --windowed --clean --noupx main.py`

4. The executable will be created in the `dist/LKIT` directory

### Notes about Antivirus Software
- Some antivirus software might flag the created executable as suspicious. This is a false positive due to the way PyInstaller packages Python applications.
- If your antivirus flags the executable, you may need to add an exception for the LKIT.exe file.

## Running Tests
The project uses Python's built-in unittest framework. There are several ways to run the tests:

### Run all tests
`python -m unittest discover tests`

### Run specific test files
`python -m unittest tests/test_models.py`
`python -m unittest tests/test_storage.py`

### Run specific test classes or methods
`python -m unittest tests.test_models.TestPerson`
`python -m unittest tests.test_models.TestPerson.test_full_name`

### Run tests with verbose output
Add the -v flag for more detailed test output:
`python -m unittest discover tests -v`