## Project Setup

### Installing the project
- Create an empty directory to house the project
- run `virtualenv env` within that directory to create a virtual environment
- run `source env/bin/activate` to initialize a virtual environment (type `deactivate` at any time to exit the environment)
- run `git clone [repository id]`
- run `cd main`
- run `pip install -r requirements.txt`

### Seed the database with pre-fabricated data
- run `python manage.py makemigrations api`
- run `python manage.py migrate`
- run `./manage.py loaddata db.json`

### Confirm passing unit tests
- run `python manage.py test`
- optional: view coverage report (71% overall) by running `pytest --cov=app`

### Run the project
- run `python manage.py runserver`
- visit http://localhost:8000/ to get started

## View the Project

### Account Information
Although there are several aspects of the site available to an unauthenticated user, most site features are only accessible when logged in. Use either of the following usernames to log in (passwords are 'password'):
- `brendan@email.com` (staff permissions)
- `dave@email.com` (standard permissions)

### Home
Permissions required: none
- Landing page
- View the three most-recent adoptions from the shelter
- See contact information and embedded google map
### Available Pets
Permissions required: none
- See all unadopted animals in card format
- Search animals by name, or filter results by animal species or age
- Click view on a card to open the detail page for that specific animal
### Pet Details
Permissions required: none / staff
- See the pet's details, including a description of the animal and a larger photo
- Click to open an adoption application
- Once an application has been submitted, the button is replaced with a notification of application status
- Return to list of all available pets
- Staff members may open a pre-populated form to edit the animal's details
- Staff members may quickly link to the animal's pending / rejected adoption applications
### Adoption Application
Permissions required: standard
- A user can submit only one adoption application per animal
- The applicaiton prompts the user to provide a detailed reason why they are a suitable candidate for adoption
- Submitting the application redirects the user to their profile, where they can see the application's status
### New Arrival
Permissions required: staff
- Staff members can open a form to upload a new animal to the database, including a photo
- If no photo is provided, a placeholder image will appear instead
- Adding an animal redirects the staff member to the available pets page
### Volunteering
Permissions required: none / staff
- See a list of upcoming volunteering activities
- If signed up, the user can see a green badge on the activity
- If the event is cancelled, the user can see a red badge on the activity
- Clicking an item in the list opens a detail page about that activity
- Staff members can open a form to add a new volunteering activity
### Volunteering Details
Permissions required: standard / staff
- See details about the upcoming volunteering activity
- If not signed up, a user can use a one-click signup feature
- If no spots are remaining, or if the event is cancelled, the user cannot sign up for the event
- Staff members can open a pre-populated form to edit any details about the activity
- Staff members can cancel an upcoming volunteering activity, preventing any user from signing up
### Adoptions
Permissions required: staff
- See a list of unadopted animals, with notification of any pending applications for any given animal
- Clicking an item in the list loads a page where all applications for that animal can be viewed
### View Specific Adoption Applications
Permissions required: staff
- Quickly link to the animal's detail page
- Browse all pending or rejected applications for a specific animal using an accordion-style menu
- Reject an application and provide a reason (confirmation required). That application moves to the rejected section
- Rejected applications can be marked for revision, which moves the application back to the pending section
- Approve an application (confirmation required). The animal will be removed from the list of available animals, displayed on the home page as a recently-adopted animal, and all remaining applications for the animal will be "rejected" with a standardized reason
### Profile and Applications
Permissions required: standard
- Open a pre-populated form to edit personal account information
- Change password with validation
- View status of submitted adoption applications