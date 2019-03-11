from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator # Used with integerfield to restrict max value
from django.db import models

# required for custom user model
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy
from .managers import CustomUserManager
from django.conf import settings # used with foreign keys related to custom user model


class CustomUser(AbstractUser):
    """
        This model overwrites the default Django user model in order to remove the username field and authenticate with e-mail.
    """

    username = None
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    first_name = models.CharField(ugettext_lazy('first name'), max_length=30, blank=False)
    last_name = models.CharField(ugettext_lazy('last name'), max_length=30, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name'] # prompted for these fields (in addition to email and password) when creating superuser

    # defines create_superuser and create_user methods
    objects = CustomUserManager()

    def __str__(self):
        return self.email

STATE_CHOICES = (
    ('AL','Alabama'),
    ('AK','Alaska'),
    ('AZ','Arizona'),
    ('AR','Arkansas'),
    ('CA','California'),
    ('CO','Colorado'),
    ('CT','Connecticut'),
    ('DE','Delaware'),
    ('FL','Florida'),
    ('GA','Georgia'),
    ('HI','Hawaii'),
    ('ID','Idaho'),
    ('IL','Illinois'),
    ('IN','Indiana'),
    ('IA','Iowa'),
    ('KS','Kansas'),
    ('KY','Kentucky'),
    ('LA','Louisiana'),
    ('ME','Maine'),
    ('MD','Maryland'),
    ('MA','Massachusetts'),
    ('MI','Michigan'),
    ('MN','Minnesota'),
    ('MS','Mississippi'),
    ('MO','Missouri'),
    ('MT','Montana'),
    ('NE','Nebraska'),
    ('NV','Nevada'),
    ('NH','New Hampshire'),
    ('NJ','New Jersey'),
    ('NM','New Mexico'),
    ('NY','New York'),
    ('NC','North Carolina'),
    ('ND','North Dakota'),
    ('OH','Ohio'),
    ('OK','Oklahoma'),
    ('OR','Oregon'),
    ('PA','Pennsylvania'),
    ('RI','Rhode Island'),
    ('SC','South Carolina'),
    ('SD','South Dakota'),
    ('TN','Tennessee'),
    ('TX','Texas'),
    ('UT','Utah'),
    ('VT','Vermont'),
    ('VA','Virginia'),
    ('WA','Washington'),
    ('WV','West Virginia'),
    ('WI','Wisconsin'),
    ('WY','Wyoming'),
)

class Volunteer(models.Model):
    """Defines a model for a volunteer (a verified user). Volunteers who are admin are treated as staff.

        Returns: __str__ userId, street_address, and phone_number
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zipcode = models.CharField(max_length=12)
    phone_number = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)])
    delete_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"User: {self.user} Street Address:{self.street_address} Phone: {self.phone_number}"


class Species(models.Model):
    """Defines an animal's species (e.g. cat, dog).

       Returns __str__ type
    """

    species = models.CharField(max_length=75)

    def __str__(self):
        return f"Species: {self.species}"


class Breed(models.Model):
    """Defines an animal's breed (e.g. domestic short hair).

       Returns __str__ breed
    """

    breed = models.CharField(max_length=75)

    def __str__(self):
        return f"Breed: {self.breed}"


class Color(models.Model):
    """Defines an animal's color.

       Returns __str__ color
    """

    color = models.CharField(max_length=40)

    def __str__(self):
        return f"Color: {self.color}"


class Animal(models.Model):
    """Defines an animal at the animal shelter.

       Returns: __str__ name, age, species, sex
    """

    name = models.CharField(max_length=16)
    # you never know if you're going to adopt out a sea turtle...
    age = models.PositiveIntegerField(validators=[MaxValueValidator(200)])
    species = models.ForeignKey(Species, on_delete=models.PROTECT)
    breed = models.ForeignKey(Breed, on_delete=models.PROTECT)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    image = models.ImageField(upload_to='media/', default="media/placeholder.jpg")
    description = models.CharField(max_length=500)
    date_arrival = models.DateTimeField(default=None, null=True, blank=True)
    date_adopted = models.DateTimeField(default=None, null=True, blank=True)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, limit_choices_to={'is_staff': True}, default=None, null=True, blank=False)

    def __str__(self):
        return f"Name: {self.name} Age: {self.age} Species: {self.species} Sex: {self.sex}"


class Application(models.Model):
    """Defines an application submitted by a user to request the adoption of an animal.

        Returns: __str__ userId, date_submitted
    """

    date_submitted = models.DateTimeField(default=None, null=True, blank=True)
    text = models.CharField(max_length=1000)
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="user")
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None, null=True, blank=True, related_name="staff")
    approved = models.BooleanField(default=None, null=True)
    reason = models.CharField(max_length=500, default=None, null=True)

    def __str__(self):
        return f"User: {self.user} Date Submitted: {self.date_submitted}"


class Activity(models.Model):
    """Defines a volunteering activity created by a staff member and applied to by users.

        Returns: __str__ name, staffId
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    date_start = models.DateTimeField(default=None, null=True, blank=False)
    date_end = models.DateTimeField(default=None, null=True, blank=False)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=None, null=True, blank=True)

    def __str__(self):
        return f"Name: {self.name} Staff: {self.staff}"

class ActivityVolunteer(models.Model):
    """Defines a join table associating volunteers with volunteer activities

    Returns: __str__ volunteerId, activityId
    """

    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f"Volunteer: {self.volunteer} Activity: {self.activity}"