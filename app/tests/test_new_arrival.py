# unittest
import unittest
from django.test import TestCase
# HTTP
from django.urls import reverse
# models
from app.models import Animal, Breed, Color, CustomUser, Species
# forms
from app.forms import AnimalForm


class NewArrivalTests(TestCase):
    """
        Models:
            Animal
            CustomUser
            Breed
            Color
            Species
        Templates:
            new_arrival.html
        Views:
            new_arrival.py
        Methods:
            setUpclass
            test_non_admin_cannot_access_form
            test_add_new_arrival
            test_add_image
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(NewArrivalTests, cls).setUpClass()

        # create breed, color, and species instances
        Breed.objects.create(
            breed = 'domestic longhair',
        )

        Color.objects.create(
            color = 'black',
        )

        Species.objects.create(
            species = 'cat',
        )

        # create user (administrator)
        CustomUser.objects.create_user(
            first_name='Test_firstname',
            last_name='Test_lastname',
            email='test_user@test.com',
            password='secret',
            is_staff=True,
        )

        # create user (non-administrator)
        CustomUser.objects.create_user(
            first_name='Test_firstname2',
            last_name='Test_lastname2',
            email='test_user2@test.com',
            password='secret2',
            is_staff=False,
        )

    def test_non_admin_cannot_access_form(self):

        # log user (not an administrator) in
        self.client.login(email='test_user2@test.com', password='secret2')

        # confirm that user is redirected (302) from page, since they are not an admin
        response = self.client.get(reverse('app:new_arrival'))
        self.assertEqual(response.status_code, 302)

    def test_add_new_arrival(self):
        """
            This test confirms that an administrator can access the new_arrival form, add a new animal to the database, and have the placeholder image appear on the Animal instance's image property.
        """

        # log user (administrator) in
        self.client.login(email='test_user@test.com', password='secret')

        # load the view once user is logged in
        response = self.client.get(reverse('app:new_arrival'))
        self.assertEqual(response.status_code, 200)

        form_data = {
            'name': 'test_animal',
            'age': '2018-03-18',
            'sex': 'F',
            'description': 'This is the pet\'s description.',
            'date_adopted': None,
            'breed': 1,
            'color': 1,
            'species': 1,
            'staff': 1,
            'arrival_date': '2019-03-18',
            'image': None,
        }

        animal_form = AnimalForm(form_data)

        # confirm validity of form
        self.assertTrue(animal_form.is_valid())

        # save form data to test database and get instance of the new animal
        new_animal = animal_form.save()

        # check that ID of saved animal is 1
        self.assertEqual(new_animal.id, 1)

        # check that image placeholder path is listed correctly (since no image was provided)
        self.assertEqual(new_animal.image, 'media/placeholder.jpg')

    def test_add_image(self):
        """
            This test confirms that an uploaded .jpg image will appear on a POSTed Animal instance's image property.
        """

        # log user (administrator) in
        self.client.login(email='test_user@test.com', password='secret')

        # test that a small photo url will post to the database
        with open("app/tests/media_test/test.jpg", "rb") as test_image:

            form_data = {
                'name': 'test_animal',
                'age': '2018-03-18',
                'sex': 'F',
                'description': 'This is the pet\'s description.',
                'date_adopted': None,
                'breed': 1,
                'color': 1,
                'species': 1,
                'staff': 1,
                'arrival_date': '2019-03-18',
                'image': test_image,
            }

            # post the form data
            response = self.client.post(reverse('app:new_arrival'), form_data)

            # confirm post response
            self.assertEqual(response.status_code, 302)

            # get instance of new_animal
            new_animal = Animal.objects.get(pk=1)

            # confirm new_animal was posted via name check
            self.assertEqual(new_animal.name, 'test_animal')

            # confirm name of test media file shows in instance (e.g. media/test_7x1jLfb.jpg)
            self.assertIn('media/test', str(new_animal.image))
