## Project Setup (Project In Progress, Complete on 3/22/2019)

### Installing the project
- Create an empty directory to house the project
- run `virtualenv env` within that directory to create a virtual environment
- run `source env/bin/activate` to initialize a virtual environment (type `deactivate` at any time to exit the environment)
- run `git clone [repository id]`
- run `cd main`
- run `pip install -r requirements.txt`

### Seed the database with pre-fabricated data
I've already created a file to populate the database.
- run `python manage.py makemigrations api`
- run `python manage.py migrate`

### Confirm passing unit tests
- run `python manage.py test`
- optional: view coverage report (71% overall) by running `pytest --cov=app`

### Run the project
- run `python manage.py runserver`
- visit http://localhost:8000/ to get started

## View the Project

### Home
Permissions required: none
### Available Pets
Permissions required: none
### Pet Details
Permissions required: none
### Adoption Application
Permissions required: authenticated
- A user can submit only one adoption application per animal
### Volunteering
Permissions required: none
### Volunteering Sign-up
Permissions required: authenticated
### New Arrival
Permissions required: staff memeber
### Adoptions
Permissions required: staff member
### Profile and Applications
Permissions required: authenticated