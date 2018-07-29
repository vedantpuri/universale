from django.db import models
from django.contrib.auth.models import User

from ffs.choices import *


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=7, default=39.99)
    image = models.FileField(upload_to='products/', null=True)
    owner = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=1, choices=Availability,
                              blank=True, default='a', help_text='Item availability')
    flag_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Student(models.Model):
    django_user = models.OneToOneField(User, unique=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    password = models.CharField(max_length=120, blank=True, help_text="Enter a password")
    college = models.CharField(max_length=1, choices=Colleges,
                               blank=True, default='u', help_text='college choice')
    email = models.EmailField(max_length=100)
    star_count = models.DecimalField(decimal_places=0, max_digits=1)
    image = models.FileField(upload_to='user_profile_picture/', null=True, blank=True)

    def __str__(self):
        return '{0}, {1}'.format(self.first_name, self.last_name)


class Flag(models.Model):
    user = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField('Product', blank=True)

    def __str__(self):
        return str(self.id)
