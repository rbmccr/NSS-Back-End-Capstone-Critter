# unittest
import unittest
from django.test import TestCase
# HTTP
from django.urls import reverse
# models
from app.models import Animal, Application, Breed, Color, CustomUser, Species
# forms
from app.forms import AnimalForm
# tools
import datetime


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
            test_unadopted_vs_adopted_in_list
            test_pending_notification_in_list
            test_staff_user_can_view_specific_applications
            test_auth_user_cannot_view_specific_applications
            test_unauth_user_cannot_view_specific_applications
            test_HTML_content_of_specific_applications_page
            test_staff_user_can_view_approval_and_cancellation_pages
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
        auth_user = CustomUser.objects.create_user(
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
        unadopted_animal = Animal.objects.create(
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

        # create pending application for the unadopted animal
        Application.objects.create(
            text = 'I want to adopt this animal.',
            staff = staff,
            approved = None,
            reason = None,
            animal = unadopted_animal,
            user = auth_user,
            date_submitted = datetime.datetime.now()
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

    def test_unadopted_vs_adopted_in_list(self):
        """
            Validate that a staff user can see the current unadopted animal in the list and cannot see the adopted animal
        """

        self.client.login(email='test_admin@test.com', password='secret')

        response = self.client.get(reverse('app:list_applications'))
        # confirm unadopted animal's name appears
        self.assertIn('test_animal_unadopted'.encode(), response.content)
        # confirm adopted animal's name does not appear
        self.assertNotIn('test_animal_adopted'.encode(), response.content)

    def test_pending_notification_in_list(self):
        """
            Validate that an animal will have a tag with a pending notification if there is an un-rejected adoption application
        """

        self.client.login(email='test_admin@test.com', password='secret')

        response = self.client.get(reverse('app:list_applications'))
        # confirm unadopted animal's name appears
        self.assertIn('1 pending</span>'.encode(), response.content)
        # delete application, reload page, and validate that pending does not appear
        application = Application.objects.get(pk=1)
        application.delete()
        response = self.client.get(reverse('app:list_applications'))
        self.assertNotIn('1 pending</span>'.encode(), response.content)

    def test_staff_user_can_view_specific_applications(self):
        """
            Validate that a staff user can see a specific animal's applications
        """

        self.client.login(email='test_admin@test.com', password='secret')

        # confirm that staff user gets 200
        response = self.client.get(reverse('app:list_specific_applications', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_auth_user_cannot_view_specific_applications(self):
        """
            Validate that an auth user cannot see a specific animal's applications
        """

        self.client.login(email='test_auth@test.com', password='secret2')

        # confirm that auth user gets 302
        response = self.client.get(reverse('app:list_specific_applications', args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_unauth_user_cannot_view_specific_applications(self):
        """
            Validate that an unauth user cannot see a specific animal's applications
        """

        # confirm that unauth user gets 302
        response = self.client.get(reverse('app:list_specific_applications', args=(1,)))
        self.assertEqual(response.status_code, 302)

    def test_HTML_content_of_specific_applications_page(self):
        """
            Confirm expected content appears on specific applications view
        """

        self.client.login(email='test_admin@test.com', password='secret')

        response = self.client.get(reverse('app:list_specific_applications', args=(1,)))
        # confirm unadopted animal's name appears
        self.assertIn('1 pending</span>'.encode(), response.content)
        self.assertIn('You\'re Viewing: test_animal_unadopted'.encode(), response.content)
        self.assertIn('Test_lastname2, Test_firstname2'.encode(), response.content)
        self.assertIn('I want to adopt this animal.'.encode(), response.content)

    def test_staff_user_can_view_approval_and_cancellation_pages(self):
        """
            Validate that a staff user can view the approval and cancellation pages
        """

        self.client.login(email='test_admin@test.com', password='secret')

        # confirm that staff user gets 200
        response = self.client.get(reverse('app:final_decision', args=(1,1,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('app:reject_application', args=(1,1,)))
        self.assertEqual(response.status_code, 200)

    def test_auth_user_cannot_view_approval_and_cancellation_pages(self):
        """
            Validate that an auth user cannot view the approval and cancellation pages
        """

        self.client.login(email='test_auth@test.com', password='secret2')

        # confirm that auth user gets 302
        response = self.client.get(reverse('app:final_decision', args=(1,1,)))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('app:reject_application', args=(1,1,)))
        self.assertEqual(response.status_code, 302)

    def test_unauth_user_cannot_view_approval_and_cancellation_pages(self):
        """
            Validate that an unauth user cannot view the approval and cancellation pages
        """

        # confirm that unauth user gets 302
        response = self.client.get(reverse('app:final_decision', args=(1,1,)))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('app:reject_application', args=(1,1,)))
        self.assertEqual(response.status_code, 302)