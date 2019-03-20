# unittest
import unittest
from django.test import TestCase
# HTTP
from django.urls import reverse
# models
from app.models import Activity, ActivityVolunteer, CustomUser, Volunteer


class VolunteeringTests(TestCase):
    """
        Models:
            Activity
            ActivityVolunteer
            CustomUser
            Volunteer
        Templates:
            list_volunteering.html
            volunteering_details.html
        Views:
            volunteering.py
        Methods:
            setUpclass
            test_unauth_user_can_view_list_activities
            test_auth_user_can_view_list_activities
            test_staff_user_can_view_list_activities
            test_unauth_user_can_view_upcoming_activity_details
            test_auth_user_can_view_upcoming_activity_details
            test_staff_user_can_view_upcoming_activity_details
            test_any_user_cannot_view_past_activity_in_list_view
            test_any_user_cannot_view_past_activity_details
            test_auth_user_volunteer_signup
            test_auth_user_volunteer_cannot_signup_for_past_activity
            test_auth_user_volunteer_cannot_signup_for_cancelled_activity
            test_auth_user_volunteer_can_revoke_signed_up_status
            test_staff_user_can_cancel_upcoming_activity
            test_staff_user_can_add_new_upcoming_activity
    """

    @classmethod
    def setUpClass(cls):
        """Creates instances of database objects before running each test in this class"""

        super(VolunteeringTests, cls).setUpClass()

        # create user (administrator)
        staff = CustomUser.objects.create_user(
            # id = 1
            first_name='Test_firstname',
            last_name='Test_lastname',
            email='test_admin@test.com',
            password='secret',
            is_staff=True,
        )

        # create staff user's volunteer table (administrator)
        Volunteer.objects.create(
            # id = 1
            street_address='987 street',
            city='Nashville',
            state='TN',
            zipcode='37205',
            phone_number=1234567777,
            user=staff,
            delete_date=None,
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

        # create user's volunteer table (not an administrator)
        Volunteer.objects.create(
            # id = 2
            street_address='123 street',
            city='Nashville',
            state='TN',
            zipcode='37203',
            phone_number=1234567890,
            user=auth_user,
            delete_date=None,
        )

        # create volunteering activity [UPCOMING]
        Activity.objects.create(
            # id = 1
            activity='Test_activity_upcoming',
            description='Test description',
            staff=staff,
            max_attendance=5,
            date='2050-03-20',
            start_time='10:00:00',
            end_time='11:00:00',
            activity_type='dogs',
            cancelled=None,
        )

        # create volunteering activity [PAST DATE]
        Activity.objects.create(
            # id = 2
            activity='Test_activity_already_occurred',
            description='Test description',
            staff=staff,
            max_attendance=5,
            date='2018-03-19',
            start_time='10:00:00',
            end_time='11:00:00',
            activity_type='general',
            cancelled=None,
        )

        # create volunteering activity [UPCOMING but CANCELLED]
        Activity.objects.create(
            # id = 3
            activity='Test_activity_cancelled',
            description='Test description',
            staff=staff,
            max_attendance=5,
            date='2050-03-19',
            start_time='10:00:00',
            end_time='11:00:00',
            activity_type='cats',
            cancelled=True,
        )

    def test_unauth_user_can_view_list_activities(self):
        """
            Validate that an unauthorized user can see list view of all upcoming volunteering activities.
        """

        # confirm that unauth user gets 200 OK
        response = self.client.get(reverse('app:list_volunteering'))
        self.assertEqual(response.status_code, 200)

    def test_auth_user_can_view_list_activities(self):
        """
            Validate that an authorized user can see list view of all upcoming volunteering activities.
        """

        # log user (not an administrator) in
        self.client.login(email='test_auth@test.com', password='secret2')
        # confirm that unauth user gets 200 OK
        response = self.client.get(reverse('app:list_volunteering'))
        self.assertEqual(response.status_code, 200)

    def test_staff_user_can_view_list_activities(self):
        """
            Validate that an authorized staff user can see list view of all upcoming volunteering activities.
        """

        # log user (not an administrator) in
        self.client.login(email='test_admin@test.com', password='secret')
        # confirm that unauth user gets 200 OK
        response = self.client.get(reverse('app:list_volunteering'))
        self.assertEqual(response.status_code, 200)

    def test_unauth_user_can_view_upcoming_activity_details(self):
        """
            Validate that an unauthorized user can see list view of all upcoming volunteering activities.
        """

        # confirm that unauth user gets 200 OK
        response = self.client.get(reverse('app:volunteering_details', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_auth_user_can_view_upcoming_activity_details(self):
        """
            Validate that an authorized user can see list view of all upcoming volunteering activities.
        """

        # log user (not an administrator) in
        self.client.login(email='test_auth@test.com', password='secret2')
        # confirm that unauth user gets 200 OK
        response = self.client.get(reverse('app:volunteering_details', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_staff_user_can_view_upcoming_activity_details(self):
        """
            Validate that an authorized staff user can see list view of all upcoming volunteering activities.
        """

        # log user (administrator) in
        self.client.login(email='test_admin@test.com', password='secret')
        # confirm that unauth user gets 200 OK
        response = self.client.get(reverse('app:volunteering_details', args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_any_user_cannot_view_past_activity_in_list_view(self):
        """
            Validate that any user cannot see past volunteering activity in the list.
        """

        # log user (administrator) in
        self.client.login(email='test_admin@test.com', password='secret')
        response = self.client.get(reverse('app:list_volunteering'))
        # confirm that response content shows upcoming event
        self.assertIn('Test_activity_upcoming'.encode(), response.content)
        # confirm that response content does not show past event
        self.assertNotIn('Test_activity_already_occurred'.encode(), response.content)
        # log admin out
        self.client.logout()

        # --------------------

        # log user (not an administrator) in
        self.client.login(email='test_auth@test.com', password='secret2')
        response = self.client.get(reverse('app:list_volunteering'))
        # confirm that response content shows upcoming event
        self.assertIn('Test_activity_upcoming'.encode(), response.content)
        # confirm that response content does not show past event
        self.assertNotIn('Test_activity_already_occurred'.encode(), response.content)
        # log auth user out
        self.client.logout()

        # --------------------

        # unauth user
        response = self.client.get(reverse('app:list_volunteering'))
        # confirm that response content shows upcoming event
        self.assertIn('Test_activity_upcoming'.encode(), response.content)
        # confirm that response content does not show past event
        self.assertNotIn('Test_activity_already_occurred'.encode(), response.content)

    def test_any_user_cannot_view_past_activity_details(self):
        """
            Validate that any user cannot see past volunteering activity detail page.
        """

        # log user (administrator) in
        self.client.login(email='test_admin@test.com', password='secret')
        response = self.client.get(reverse('app:volunteering_details', args=(2,)))
        # confirm user is redirected from page (302)
        self.assertEqual(response.status_code, 302)
        # log admin out
        self.client.logout()

        # --------------------

        # log user (not an administrator) in
        self.client.login(email='test_auth@test.com', password='secret2')
        response = self.client.get(reverse('app:volunteering_details', args=(2,)))
        # confirm user is redirected from page (302)
        self.assertEqual(response.status_code, 302)
        # log auth user out
        self.client.logout()

        # --------------------

        # unauth user
        response = self.client.get(reverse('app:volunteering_details', args=(2,)))
        # confirm user is redirected from page (302)
        self.assertEqual(response.status_code, 302)

    def test_auth_user_volunteer_signup(self):
        """
            Confirm that an authorized user can sign up for a volunteering activity
        """

        # log user (not an administrator) in
        self.client.login(email='test_auth@test.com', password='secret2')
        # clicking sign up button requests the url below
        response = self.client.get(reverse('app:volunteering_signup', args=(1,)))
        # user is redirected with 302 code for any return statement in volunteering_signup
        self.assertEqual(response.status_code, 302)
        # confirm a database join table was created in ActivityVolunteer (i.e. length of 1 = 1)
        result = len(ActivityVolunteer.objects.all())
        self.assertEqual(result,1)

    def test_auth_user_volunteer_cannot_signup_for_past_activity(self):
        """
            Confirm that an authorized user cannot sign up for a past volunteering activity
        """

        # log user (not an administrator) in
        self.client.login(email='test_auth@test.com', password='secret2')
        # clicking sign up button requests the url below
        response = self.client.get(reverse('app:volunteering_signup', args=(2,)))
        # confirm user is redirected (again, this happens for any signup return statement, so it isn't that valuable to test)
        self.assertEqual(response.status_code, 302)
        # confirm a database join table was NOT created in ActivityVolunteer (i.e. result is empty)
        result = len(ActivityVolunteer.objects.all())
        self.assertEqual(result,0)

    def test_auth_user_volunteer_cannot_signup_for_cancelled_activity(self):
        """
            Confirm that an authorized user cannot sign up for a cancelled volunteering activity
        """

        # log user (not an administrator) in
        self.client.login(email='test_auth@test.com', password='secret2')
        # clicking sign up button requests the url below
        response = self.client.get(reverse('app:volunteering_signup', args=(3,)))
        # confirm user is redirected (again, this happens for any signup return statement, so it isn't that valuable to test)
        self.assertEqual(response.status_code, 302)
        # confirm a database join table was NOT created in ActivityVolunteer (i.e. result is empty)
        result = len(ActivityVolunteer.objects.all())
        self.assertEqual(result,0)

    def test_auth_user_volunteer_can_revoke_signed_up_status(self):
        """
            Confirm that an authorized user can remove their signed up status
        """

        # log user (not an administrator) in
        self.client.login(email='test_auth@test.com', password='secret2')
        # clicking sign up button requests the url below
        self.client.get(reverse('app:volunteering_signup', args=(1,)))
        # confirm a database join table was created in ActivityVolunteer (i.e. length of 1 = 1)
        result = len(ActivityVolunteer.objects.all())
        self.assertEqual(result,1)
        # clicking cancel reservation button requests the url below
        self.client.post(reverse('app:volunteering_signup', args=(1,)))
        # confirm a database join table was removed from ActivityVolunteer (i.e. length is empty)
        result = len(ActivityVolunteer.objects.all())
        self.assertEqual(result,0)

    def test_staff_user_can_cancel_upcoming_activity(self):
        """
            Validate that a staff user can cancel an upcoming activity
        """

        self.client.login(email='test_admin@test.com', password='secret')
        # GET cancel url path
        response = self.client.get(reverse('app:cancel_volunteering', args=(1,)))
        self.assertEqual(response.status_code, 200)
        # POST to cancel url path (i.e. click confirmation button)
        response = self.client.post(reverse('app:cancel_volunteering', args=(1,)))
        # confirm database table shows cancelled property of True
        activity = Activity.objects.get(pk=1)
        self.assertTrue(activity.cancelled)

    def test_staff_user_can_add_new_upcoming_activity(self):
        """
            Validate that a staff user can cancel an upcoming activity
        """

        self.client.login(email='test_admin@test.com', password='secret')
        # GET add volunteering path and check for 200
        response = self.client.get(reverse('app:add_volunteering'))
        self.assertEqual(response.status_code, 200)
        # POST to add volunteering url path (i.e. submit form)

        form_data = {
            'activity': 'new_upcoming_activity',
            'activity_type': 'cats',
            'date': '2050-03-20',
            'description': 'a new activity',
            'start_time': '10:00:00',
            'end_time': '14:00:00',
            'max_attendance': 15,
        }

        response = self.client.post(reverse('app:add_volunteering'), form_data)
        # confirm database table shows cancelled property of True
        activity = Activity.objects.get(pk=4)