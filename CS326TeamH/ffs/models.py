from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=7, default=39.99)
    image = models.FileField(upload_to='products/', null=True, blank=True)
    owner = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    college_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    star_count = models.DecimalField(decimal_places=0, max_digits=1)
    image = models.FileField(upload_to='user_profile_picture/', null=True, blank=True)

    def __str__(self):
        return '{0}, {1}'.format(self.first_name, self.last_name)
