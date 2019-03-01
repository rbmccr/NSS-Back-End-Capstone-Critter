from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator # Used with integerfield to restrict max value
from django.db import models

class Volunteer(models.Model):
    """Defines a model for a volunteer (a verified user). Volunteers who are admin are treated as staff.

        Returns: __str__ userId, street_address, and phone_number
    """

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=12)
    phone_number = models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])
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

    name = models.CharField(max_length=75)
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
    staff = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Name: {self.name} Age: {self.age} Species: {self.species} Sex: {self.sex}"


class Application(models.Model):
    """Defines an application submitted by a user to request the adoption of an animal.

        Returns: __str__ userId, date_submitted
    """

    date_submitted = models.DateTimeField(default=None, null=True, blank=True)
    text = models.CharField(max_length=1000)
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # note that the 'staff' attribute is effectively a foreign key, but it cannot be a foreign key field relative to the User in this model, or it conflicts with the 'user' attribute. When an application is approved or rejected, the staff member who made the decision will have their id manually added to the field in the model
    staff = models.PositiveSmallIntegerField()
    approved = models.BooleanField(default=None, null=True)

    def __str__(self):
        return f"User: {self.user} Date Submitted: {self.date_submitted}"