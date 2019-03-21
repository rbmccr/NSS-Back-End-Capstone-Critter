## About the Project
<em>Critter</em> is an application designed to support a small, limited-resource animal shelter that may not have the financial or technical ability to develop a website of its own. It is written in Python and Django with Bootstrap styling.

Features of the application vary, depending on permissions. Anyone can search for animals, view an animal’s details, and see upcoming volunteering opportunities. Registered users can apply to adopt animals and monitor an application’s status on their profile. They can also easily sign up to volunteer. Site administrators can manage animals that appear on the site, review applications for a specific animal before approving or declining them, and organize volunteering activities.

I have a big heart for animals, and I personally understand the immense impact a pet can have on a person’s quality of life. <em>Critter</em> was an opportunity for me to create a deployable template that I can offer to animal shelters.

### Languages, Libraries, and Frameworks
<p float="left">
  <img src="https://energyframeworks.com/wp-content/uploads/2013/12/html5-css-javascript-logos.png" height="75" alt="html css javascript" title="html css javascript">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://js.foundation/wp-content/uploads/sites/33/2017/02/jquery.png" height="70" alt="jQuery" title="jQuery">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1024px-Python-logo-notext.svg.png" height="75" alt="Python" title="Python"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="http://dlyapun.com/static/images/django.png" height="75" alt="Django" title="Django"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://upload.wikimedia.org/wikipedia/commons/e/ea/Boostrap_logo.svg" height="70" alt="Bootstrap" title="Bootstrap"/>
</p>

### Development Tools
<p float="left">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Visual_Studio_Code_1.18_icon.svg/1200px-Visual_Studio_Code_1.18_icon.svg.png" height="75" alt="VS Code"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://git-scm.com/images/logos/downloads/Git-Icon-Black.png" height="75" alt="git" title="git"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://assets.ubuntu.com/v1/29985a98-ubuntu-logo32.png" height="75" alt="ubuntu" title="ubuntu"/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://docs.pytest.org/en/latest/_static/pytest1.png" height="75" alt="pytest" title="pytest"/>
</p>

## Project Setup

### Installing the project
- Create an empty directory to house the project
- run `virtualenv env` within that directory to create a virtual environment
- run `source env/bin/activate` to initialize a virtual environment (type `deactivate` at any time to exit the environment)
- run `git clone [repository id]`
- run `cd main`
- run `pip install -r requirements.txt`

### Seed the database with pre-fabricated data
- run `./django_data.sh app db.json`. This will make migrations and seed the database with content

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

### Login / Registration (navbar)
Permissions required: none
- A user who is not registered can complete a form with their contact information to create an account
- An existing user can log in

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