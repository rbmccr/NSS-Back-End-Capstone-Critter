# unittest
import unittest
from django.test import TestCase
# HTTP
from django.urls import reverse
# models
from app.models import Animal, Breed, Color, CustomUser, Species


class AnimalDetailTests(TestCase):
    """
        Models:
            Animal
            CustomUser
            Breed
            Color
            Species
        Templates:
            animal_detail.html
        Views:
            available_animals.py
        Methods:
            setUpClass
            test_unauth_user_can_view_animal_detail
            test_auth_user_can_view_animal_detail
            test_staff_user_can_view_animal_detail
            test_validate_detail_page_HTML_content
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(AnimalDetailTests, cls).setUpClass()

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

        # create user (administrator)
        staff = CustomUser.objects.create_user(
            first_name='Test_firstname',
            last_name='Test_lastname',
            email='test_admin@test.com',
            password='secret',
            is_staff=True,
        )

        # create animal instance
        Animal.objects.create(
            name = 'test_animal',
            age = '2018-03-18',
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

        # create user
        CustomUser.objects.create_user(
            first_name='Test_firstname2',
            last_name='Test_lastname2',
            email='test_auth@test.com',
            password='secret2',
            is_staff=False,
        )

    def test_unauth_user_can_view_animal_detail(self):
        """
            Confirms that an unauthenticated user can see an animal's detail page.
        """

        # confirm that unauth user gets 200 OK
        response = self.client.get(reverse('app:animal_detail', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_auth_user_can_view_animal_detail(self):
        """
            Confirms that an authenticated user can see an animal's detail page.
        """

        # log user (not an administrator) in
        self.client.login(email='test_auth@test.com', password='secret2')

        # confirm that standard auth user gets 200 OK
        response = self.client.get(reverse('app:animal_detail', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_staff_user_can_view_animal_detail(self):
        """
            Confirms that an authenticated staff-level user can see an animal's detail page.
        """

        # log user (administrator) in
        self.client.login(email='test_admin@test.com', password='secret')

        # confirm that admin user gets 200 OK
        response = self.client.get(reverse('app:animal_detail', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_validate_detail_page_HTML_content(self):
        """
            Validates that expected HTML content exists on animal detail view
        """

        response = self.client.get(reverse('app:animal_detail', args=(1,)))

        # validate image placeholder
        self.assertIn("<img src='/media/placeholder.jpg'".encode(), response.content)
        # validate animal description
        self.assertIn("<li class='list-group-item'>This is the pet&#39;s description.</li>".encode(), response.content)
        # validate apply for adoption button
        self.assertIn("<a class='btn btn-outline-dark' href=\"/pets/adopt/1\">".encode(), response.content)