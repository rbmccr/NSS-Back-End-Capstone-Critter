# unittest
import unittest
from django.test import TestCase
# HTTP
from django.urls import reverse
# models
from app.models import Animal, Application, Breed, Color, CustomUser, Species
# forms
from app.forms import AnimalForm


class AdminAdoptionsTest(TestCase):
    """
        Models:
            Animal,
            Application,
            Breed,
            Color,
            CustomUser,
            Species
        Templates:
            list_animals.html
        Views:
            adoptions.py
        Methods:
            setUpclass
            test_staff_can_view_list_of_animals
            test_auth_user_cannot_view_list_of_animals
            test_unauth_user_cannot_view_list_of_animals
            test_HTML_content_of_list
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(AdminAdoptionsTest, cls).setUpClass()

        # create user (administrator)
        staff = CustomUser.objects.create_user(
            # id = 1
            first_name='Test_firstname',
            last_name='Test_lastname',
            email='test_admin@test.com',
            password='secret',
            is_staff=True,
        )

        # create user (not an administrator)
        CustomUser.objects.create_user(
            # id = 2
            first_name='Test_firstname2',
            last_name='Test_lastname2',
            email='test_auth@test.com',
            password='secret2',
            is_staff=False,
        )

        # create breed, color, and species instances
        breed = Breed.objects.create(
            breed = 'domestic longhair',
        )

        color = Color.objects.create(
            color = 'black',
        )

        species = Species.objects.create(
            species = 'cat',
        )

        # create animal instance [UNADOPTED]
        Animal.objects.create(
            name = 'test_animal_unadopted',
            age = '2018-03-17',
            sex = 'F',
            description = 'This is the pet\'s description.',
            date_adopted = None,
            breed = breed,
            color = color,
            species = species,
            staff = staff,
            arrival_date = '2019-03-18',
            # note no image provided
        )

        # create animal instance [ADOPTED]
        Animal.objects.create(
            name = 'test_animal_adopted',
            age = '2018-03-18',
            sex = 'M',
            description = 'This is the pet\'s description.',
            date_adopted = '2019-03-20',
            breed = breed,
            color = color,
            species = species,
            staff = staff,
            arrival_date = '2019-03-17',
            # note no image provided
        )

    def test_staff_can_view_list_of_animals(self):
        """
            Validate that a staff user can see list view of all animals
        """

        self.client.login(email='test_admin@test.com', password='secret')

        # confirm that unauth user gets 200 OK
        response = self.client.get(reverse('app:list_applications'))
        self.assertEqual(response.status_code, 200)

    def test_auth_user_cannot_view_list_of_animals(self):
        """
            Validate that a authorized user cannot see list view of all animals
        """

        self.client.login(email='test_auth@test.com', password='secret2')

        # confirm that unauth user gets 302
        response = self.client.get(reverse('app:list_applications'))
        self.assertEqual(response.status_code, 302)

    def test_unauth_user_cannot_view_list_of_animals(self):
        """
            Validate that an unauthorized user cannot see list view of all animals
        """

        # confirm that unauth user gets 302
        response = self.client.get(reverse('app:list_applications'))
        self.assertEqual(response.status_code, 302)

    def test_HTML_content_of_list(self):
        """
            Validate that a staff user can see the current unadopted animal in the list and cannot see the adopted animal
        """

        self.client.login(email='test_admin@test.com', password='secret')

        response = self.client.get(reverse('app:list_applications'))
        # confirm unadopted animal's name appears
        self.assertIn('test_animal_unadopted'.encode(), response.content)
        # confirm adopted animal's name does not appear
        self.assertNotIn('test_animal_adopted'.encode(), response.content)