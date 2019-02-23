# About the Project

### Installing the project
- Create an empty directory to house your new project
- run `virtualenv env` to create a virtual environment within that directory
- run `source env/bin/activate` to initialize a virtual environment (type `deactivate` at any time to exit the environment)
- run `git clone [repository id]`
- run `cd BangazonAPI`
- run `pip install -r requirements.txt`

### Seed the database with pre-fabricated data
We've already created a file to populate the database file.
- run `python manage.py makemigrations api`
- run `python manage.py migrate`
