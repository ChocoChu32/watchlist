# Watchlist

A simple movie watchlist application built with Flask.

Demo: http://chocochu.pythonanywhere.com

## Features

- **Movie Management**: Add, edit, and delete movies from your watchlist.
- **User Authentication**: Secure login and logout functionality.
- **Settings**: Update user profile information.
- **Responsive Design**: Simple and clean interface.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ChocoChu32/watchlist.git
   cd watchlist
   ```

2. Install dependencies with uv:

   ```bash
   uv sync
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

## Usage

### Generate Fake Data

You can generate some fake data (movies and a default admin user) for testing purposes:

```bash
flask forge
```

_Note: The default admin user created by `forge` is username: `admin`, password: `123456`._

### Run the Application

Start the development server:

```bash
flask run
```

Open your browser and visit [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Testing

This project uses `pytest` for testing. To run the tests:

```bash
python -m pytest
```

To run tests with coverage report:

```bash
python -m pytest --cov=watchlist
```

Example output:

```bash
============================= test session starts ==============================
collected 15 items                                                             

tests/test_watchlist.py::test_app_exist PASSED                           [  6%]
tests/test_watchlist.py::test_app_is_testing PASSED                      [ 13%]
tests/test_watchlist.py::test_404_page PASSED                            [ 20%]
tests/test_watchlist.py::test_index_page PASSED                          [ 26%]
tests/test_watchlist.py::test_create_item PASSED                         [ 33%]
tests/test_watchlist.py::test_update_item PASSED                         [ 40%]
tests/test_watchlist.py::test_delete_item PASSED                         [ 46%]
tests/test_watchlist.py::test_login_protect PASSED                       [ 53%]
tests/test_watchlist.py::test_login PASSED                               [ 60%]
tests/test_watchlist.py::test_logout PASSED                              [ 66%]
tests/test_watchlist.py::test_settings PASSED                            [ 73%]
tests/test_watchlist.py::test_initdb_command PASSED                      [ 80%]
tests/test_watchlist.py::test_forge_command PASSED                       [ 86%]
tests/test_watchlist.py::test_admin_command PASSED                       [ 93%]
tests/test_watchlist.py::test_admin_command_update PASSED                [100%]

================================ tests coverage ================================

Name                               Stmts   Miss  Cover
------------------------------------------------------
watchlist/__init__.py                 23      0   100%
watchlist/blueprints/__init__.py       0      0   100%
watchlist/blueprints/auth.py          28      0   100%
watchlist/blueprints/main.py          60      1    98%
watchlist/commands.py                 42      1    98%
watchlist/errors.py                   11      2    82%
watchlist/extensions.py               13      3    77%
watchlist/models.py                   20      0   100%
watchlist/settings.py                 15      0   100%
------------------------------------------------------
TOTAL                                212      7    97%
============================== 15 passed in 1.93s ==============================
```
