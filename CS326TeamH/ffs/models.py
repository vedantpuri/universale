from django.db import models

# Create your models here.


class ProductQuerySet(models.query.QuerySet):
    def search(self, query):
        lookups = (Q(title__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query))
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()

        return None

class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=7, default=39.99)
    image = models.FileField(upload_to='products/', null=True, blank=True)
    owner = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    Availability = (
        ('a', 'Available'),
        ('s', 'Sold'),
    )
    status = models.CharField(max_length=1, choices=Availability, blank=True, default='a', help_text='Item availability')

    def __str__(self):
        return self.title

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    password = models.CharField(max_length=120, blank=True, help_text="Enter a password")
    College = (
        ('u', 'Umass Amherst'),
        ('a', 'Amherst College'),
        ('s', 'Smith College'),
        ('m', 'Mount Holyoke College'),
        ('h', 'Hamshire College'),
    )

    college = models.CharField(max_length=1, choices=College, blank=True, default='u', help_text='college choice')
    email = models.EmailField(max_length=100)
    star_count = models.DecimalField(decimal_places=0, max_digits=1)
    image = models.FileField(upload_to='user_profile_picture/', null=True, blank=True)

    def __str__(self):
        return '{0}, {1}'.format(self.first_name, self.last_name)

class Flag(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField('Product', blank=True)

    def __str__(self):
        return str(self.id)
