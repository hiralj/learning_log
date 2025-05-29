## Intro
Learning Logs is a `Django` project from the book - Python Crash Course, by Eric Matthes. 

### What's Django?
Django is a Python-based web framework which comes with "batteries included". What that means is that it comes built-in with many other things needed to build a website - it's own lightweight web server, ORM (= Object Relational Mapping) with support for PostgreSQL, MySQL, MariaDB, etc, Admin functionalities / pages, etc. `Flask` and `Bottle` are the lightweight siblings / alternatives of Django.

## Setup
- You need a virtual environment. So in your workspace:
  - `python3 -m venv <venv_name>`
  - [venv module](https://pymotw.com/3/venv/index.html) is now part of standard library.
  - Once venv is created, you need to "activate" it - meaning that:
    - libraries, commands, etc within the venv are now available.
    - Things downloaded (say using `pip`) will be available to this venv, but not outside.
  - To activate, `source ll_env/bin/activate` - where 'll_env' is the name given above to virtual environment.
  - `deactivate` command is used to essentially come out of the venv's effect.
- Post activating venv (this is confirmed by the venv name showing at the start of terminal prompt, in parenthesis), install django and start a project:
  - `pip install --upgrade pip`
  - `pip install django`
  - `django-admin startproject ll_project .`
    - The `.` at the end mentions which directory to start the project into.
    - This creates following:
      - `manage.py` - a CLI utility for admin tasks. It is then used in-place of django-admin.py.
      - `ll_project/` folder, containing:
        - `__init__.py` - empty file, tells that this directory is Python package.
        - `urls.py` - URL patterns.
        - `settings.py` - config.
        - `wsgi.py` - for WSGI-compatible web servers (e.g.: Gunicorn).

## Commands
Here are some useful commands:
- `python manage.py runserver`
  - From within the venv, you don't need `python3`. Just `python` works and it points to the same python interpreter used to create the venv (i.e. python3 here)
- `python manage.py migrate <app_name>` - to actually make necessary database changes to the corresponding application.
  - The `app_name` can be of the *application* you created within the *project*.
    - **Think of app as having their own URL prefix**.
    - e.g.: "/accounts/login", "/accounts/logout", "/accounts/register" --> part of "accounts" app.
    - e.g.: "/topics", "/topic/<int:topic_id>", "/new_topic", etc --> empty prefix - part of "learning_logs" app.
    - e.g.: "/telemetry/dashboard",.. -- part of "telemetry" app.
  - Or it can be one of the default django app - auth, admin, sessions, staticfiles, etc (defined in <project>/settings.py).
  - If you don't specify <app_name>, all (from setting.py) are taken.
- `python manage.py makemigrations <app_name>` - to prepare / construct changes to be made to DB.
  - This will create migration files within `<workspace>/<app_name>/migrations/` directory.
  - e.g.: `0001_initial.py`
  - Here too <app_name> is optional.
- `python manage.py sqlmigrate <app_name> <migration_filename_initial_numbers>` - see the SQL statements that will be run during `migrate` command.
  - e.g.: `python manage.py sqlmigrate learning_logs 0001`
- Wait, we did't yet create our own app (within the project yet). There are only default ones. To create:
- `python manage.py startapp <app_name>`
 
## Misc
- This also downloads and uses the Bootstrap library for styling the pages.
- You basically follow the steps on chapters 18, 19 and 20 of the book.
- Some of the changes are for deployment to *Platform.sh* - a hosting provider.
- SQLite is used - which runs on the same machine as that of application.
  - hence, it's not applicable for serverless solution such as AWS Lambda.
