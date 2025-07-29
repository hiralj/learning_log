# Intro
Learning Logs is a `Django` project from the book - Python Crash Course, by Eric Matthes. 

## What's Django?
Django is a Python-based web framework with "batteries included", meaning it comes with many other things built-in, needed to build a website. Such as it's own lightweight web server, ORM (= Object Relational Mapping) with support for PostgreSQL, MySQL, MariaDB, etc, Admin functionalities / pages, etc. `Flask` and `Bottle` are the lightweight siblings / alternatives of Django.

### Doc
- This index seems useful list of topics / subtopics: https://docs.djangoproject.com/en/5.2/topics/
- Django source code? Here it is: https://github.com/django/django

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

# EC2->RDS, on dev server
## Code
### Secret out of source code
`settings.py` file has `SECRET_KEY`, `DB_PASSWORD`,etc defined. It is quite understandable that such sensitive strings must not be present in code, as it will be committed to version control systems such as GitHub, and becomes accessible to broader audience. 

One way to deal with this is to use environment variables.
- `python-dotenv` module is used to read these variables from `.env` file, present in user directory.
- This `.env` file is not committed to the repository.
- It's read like so: 
```
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
```
- And the `.env` file looks like:
```
DJANGO_SECRET_KEY = 'some_random_string'
...
```
- This is done in local, changes in settings.py is committed to repository. But the environment variables file remains local.

### Only used dependencies
- `pipreqs ll_project` created a `requirements.txt` file containing only those dependencies used (with `import`) in the project.
- Simply using `pip freeze > requirements.txt` will create a file containing all the dependencies installed in the venv - whether they are actually used or not.
## Infra
- The flow is "VPC --> EC2 --> Subnet Group --> RDS".
- VPC is created, using "VPC and more" option in console. Select 2 AZs, 4 subnets (2 private, 2 public). IGW and route tables are automatically created and attached.
- EC2 instance is created with SG containing Inbound rules allowing SSH and custom TCP from 8000 port.
- Subnet Group is created with 2 private subnets from above VPC.
- RDS instance is created with SG containing Inbound rules allowing TCP from EC2 instance.
  - Postgres in free tier.
  - Enabled IAM auth along with password (planning to use it later).
  - Instance name: 'learning-logs-db-instance'
  - DB name: 'learning_logs'
  - Master username: 'postgres'
  - Password: RDS autogenerated. This can be copied only once post instance creation.
## EC2 setup
### OS specific setup
- Apparently, AL2023 comes with python3.9 pre-installed. Python3.10 needs to be manually installed. Also, the required SSL modules need to be installed.
```
sudo dnf groupinstall "Development Tools" -y

sudo dnf install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel libffi-devel wget make -y

cd /usr/src
sudo wget https://www.python.org/ftp/python/3.10.10/Python-3.10.10.tgz
sudo tar xzf Python-3.10.10.tgz
cd Python-3.10.10

sudo ./configure --enable-optimizations
sudo make altinstall

python3.10 --version
pip3.10 --version

python3.10 -c "import ssl; print(ssl.OPENSSL_VERSION)"
```
- The last command should print the version of SSL, verifying that Python's SSL module is installed.
- Do install `git` as well.
```
sudo dnf install git -y
```
- Such OS specific setup can be avoided with Docker (someone [recommended on reddit](https://www.reddit.com/r/aws/comments/1911jmv/how_can_i_get_python_310_on_an_ec2_instance/))
### App setup
- Clone the repo in home directory.

```
git clone <repo_url>
```
- Create a virtual environment.
```
python3.10 -m venv ll_env
```
- Activate the venv.
```
source ll_env/bin/activate
```
- Install the required dependencies.
```
pip install -r ll_project/requirements.txt
```
- Create a `.env` file with the required environment variables.
```
DJANGO_SECRET_KEY='<secret_string>'
DB_NAME='learning_logs'
DB_USER='postgres'
DB_PASSWORD='<post_RDS_instance_creation>'
DB_HOST='<RDS_instance_endpoint>'
DB_PORT='5432'
DJANGO_ALLOWED_HOSTS='<EC2_instance_public_IP>'
DJANGO_DEBUG=True
```
- Run the migrations.
```
python ll_project/manage.py migrate
```
- Run the server, the last parameter to tell Django to listen on all network interfaces, making it accessible from outside. Othwerwise, it will only listen on 127.0.0.1, which doesn't work for EC2.
```
python manage.py runserver 0.0.0.0:8000
```
- This does not yet use the production recommended WSGI server, **Gunicorn**.
