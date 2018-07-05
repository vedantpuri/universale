from django.contrib import admin

# Register your models here.
from .models import Product
from .models import User
from .models import Flag

admin.site.register(Product)
admin.site.register(User)
admin.site.register(Flag)
