from django.urls import path
from . import views
from ffs.views import product_list_view
from ffs.views import user_view
from ffs.views import search_view

urlpatterns = [
	path('products/', product_list_view),
	path('user/', user_view),
	path('search/', search_view)

]
