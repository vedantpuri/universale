from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Student
from .models import Flag

admin.site.register(Product)
admin.site.register(Student)
admin.site.register(Flag)
