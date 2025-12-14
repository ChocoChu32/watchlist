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
tests/test_watchlist.py ...............         [100%]
______________________________________________________
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
```
