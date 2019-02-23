# About the Project (In Progress, Complete on 3/22/2019)

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

### Adoption Applications
- A user can submit only one adoption application per animal. Additionally, if a shelter staff member rejects the application, then the user who submitted the application will still not be able to submit another.
- If an application is approved for a particular animal, then:
-- Remaining applications in the system for that animal will not be visible by shelter staff members