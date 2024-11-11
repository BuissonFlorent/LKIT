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