from django.urls import path
from . import views
from ffs.views import product_list_view
from ffs.views import user_view
from ffs.views import search_view
from ffs.views import flagged_view
from ffs.views import landing_view
from ffs.views import upload_view
from ffs.views import edit_profile_view
from ffs.views import add_to_flagged

urlpatterns = [
	path('user/', user_view, name='user'),
	path('search/', search_view, name='search'),
	path('flagged/', flagged_view, name='flag'),
	path('user/add/', add_to_flagged, name='flag_add'),
	path('upload/', upload_view, name='upload'),
	path('edit_profile/', edit_profile_view, name="user_edit"),
	path('', landing_view, name='home')
]
