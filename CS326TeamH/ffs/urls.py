from django.urls import path
from . import views
from ffs.views import product_list_view

urlpatterns = [
	path('products/', product_list_view)
]